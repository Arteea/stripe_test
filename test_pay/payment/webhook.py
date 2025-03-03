import stripe
from django.http import HttpResponse, JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views import View

from .models import Order

import os
from dotenv import load_dotenv

load_dotenv()

import logging

logger = logging.getLogger(__name__)


stripe.api_key = os.getenv('STRIPE_API_KEY')
ENDPOINT_SECRET = os.getenv('STRIPE_ENDPOINT_SECRET')


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):

    def post(self, request, *args, **kwargs):
        payload = request.body.decode('utf-8')
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = ENDPOINT_SECRET     # Секрет для проверки подписи

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )

            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']                # Получаем объект PaymentIntent
                metadata = payment_intent['metadata']
                order_id = metadata.get('order_id')
                current_order = Order.objects.get(id = order_id)
                current_order.is_paid = True
                current_order.save()
            
            elif event["type"] == "checkout.session.completed":
                session = event["data"]["object"]
                order_id = session.get("metadata", {}).get("order_id")
                current_order = Order.objects.get(id = order_id)
                current_order.is_paid = True
                current_order.save()

            return JsonResponse({'status': 'success'}, status=200)

        except ValueError as e:
    # Invalid payload
            print('Error parsing payload: {}'.format(str(e)))
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print('Error verifying webhook signature: {}'.format(str(e)))
            return HttpResponse(status=400)

