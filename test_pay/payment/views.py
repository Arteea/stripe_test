from typing import Any

import json

from django.conf import settings

from django.db.models.base import Model as Model

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Item, Order, OrderItem, Tax, Discount
import stripe

import os
from dotenv import load_dotenv

load_dotenv()


stripe.api_key = os.getenv("STRIPE_API_KEY")


import logging

logger = logging.getLogger(__name__)



class ItemDetailView(DetailView):

    model = Item
    template_name = "item.html"

    ### Для обращения в шаблоне через item
    context_object_name = "item"

    def get_object(self, queryset=None):
        item_id = self.kwargs.get("id")
        return get_object_or_404(Item, id=item_id)



class CheckoutService:
    @staticmethod
    def create_tax(tax):
        return stripe.TaxRate.create(
            display_name=tax.name,
            percentage=float(tax.percentage),
            inclusive=False,
        )

    @staticmethod
    def create_discount(discount,order):
        overall_percentage = 0
        for discount in order.discount.all():
            overall_percentage+=discount.percentage
        if overall_percentage:            
            return stripe.Coupon.create(
            percent_off=overall_percentage,
        )

    @staticmethod
    def create_checkout_session(line_items, discounts, success_url, cancel_url,metadata):
        return stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            discounts=discounts,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata,

        )


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get("id")
        item = Item.objects.get(id=item_id)
        new_order = self.create_order(item)

        try:
            taxes = self.get_taxes(new_order)
            discounts = self.get_discounts(new_order)
            line_items = self.get_line_items(item, taxes)

            checkout_session = CheckoutService.create_checkout_session(
                line_items=line_items,
                discounts=discounts,
                success_url="http://localhost:8000/success",
                cancel_url="http://localhost:8000/cancel",
                metadata={"order_id": new_order.id}
            )

            return JsonResponse({"session_id": checkout_session.id}, status=303)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def create_order(self, item):
        new_order = Order.objects.create()
        OrderItem.objects.create(order=new_order, item=item)
        new_order.tax = Tax.objects.get(id=1)

        if item.name == "Кресло":
            new_order.discount.add(Discount.objects.get(id=2))
        elif item.name == "Стул":
            new_order.discount.add(Discount.objects.get(id=1))

        return new_order

    def get_taxes(self, order):
        taxes = []
        if order.tax:
            tax = CheckoutService.create_tax(order.tax)
            taxes.append(tax.id)
        return taxes

    def get_discounts(self, order):
        discounts = []
        if order.discount:
            discount = CheckoutService.create_discount(order.discount,order)
            if discount:
                discounts.append({"coupon": discount.id})
        return discounts

    def get_line_items(self, item, taxes):
        return [
            {
                "quantity": 1,
                "tax_rates": taxes,
                "price_data": {
                    "currency": item.currency,
                    "unit_amount": int(item.price) * 100,
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                },
            }
        ]


class ItemsListView(ListView):

    model = Item
    template_name = "items_list.html"


class CreateOrderView(View):

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        order = Order.objects.create()

        for item_data in data["items"]:

            item_id = item_data.get("id")
            quantity = item_data.get("quantity")
            item = Item.objects.get(id=int(item_id))

            OrderItem.objects.create(order=order, item=item, quantity=quantity)

        total_price = order.calculate_full_price()
        order_data = {"total_price": float(total_price), "order_id": order.id}

        return JsonResponse(order_data, status=200)


class CreateCheckoutIntentView(View):

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        logger.info(data)
        order_id =data.get("order_id")
        order = Order.objects.get(id = order_id)
        price = data.get("price")
        

        try:
            
            tax_amount = CreatePaymentIntent.determine_tax_amount(order,price)

            price+=tax_amount

            discount_amount = CreatePaymentIntent.determine_discount_amount(order,price)

            price-=discount_amount

            payment_intent = stripe.PaymentIntent.create(
                amount=int(price * 100),
                currency="usd",
                payment_method_types=["card"],
                metadata={"order_id": order_id},
            )

            return JsonResponse({"clientSecret": payment_intent.client_secret, "price": payment_intent.amount, 
                                 "currency": payment_intent.currency, "discount": discount_amount, "tax":tax_amount})
        except Exception as e:
            logger.error(str(e))
            return JsonResponse({"error": str(e)}, status=400)


class CreatePaymentIntent:

    @staticmethod
    def determine_tax_amount(order,order_price):    
        tax_amount = 0
        if not order.tax:
            order.tax = Tax.objects.get(id=1)
            order.save
        tax_amount = (order.tax.percentage*order_price)/100

        return tax_amount
    
    @staticmethod
    def determine_discount_amount(order,order_price):

        discount_amount = 0
        if order_price>10000:
            discount = Discount.objects.get(id=3)
            order.discount.add(discount)
            discount_amount += (order_price*discount.percentage)/100

        for item in order.items.all():

            if item.name == "Кресло":
                discount = Discount.objects.get(id=2)
                order.discount.add(discount)
                discount_amount += (order_price*discount.percentage)/100

            elif item.name == "Стул":
                discount = Discount.objects.get(id=3)
                order.discount.add(discount)
                discount_amount += (order_price*discount.percentage)/100
            
        return discount_amount
        






def payment_success(request):
    return render(request, "success.html")


def payment_failed(request):
    return render(request, "cancel.html")
