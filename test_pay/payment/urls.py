from django.urls import path
from .views import ItemDetailView,CreateCheckoutSessionView,ItemsListView,CreateOrderView,CreateCheckoutIntentView,payment_failed,payment_success
from .webhook import StripeWebhookView

app_name = 'payment'

urlpatterns = [
    path('item/<int:id>/',ItemDetailView.as_view(),name = "item_details"),
    path('buy/<int:id>/',CreateCheckoutSessionView.as_view(),),
    path('items_list/',ItemsListView.as_view(),),
    path('create_order/',CreateOrderView.as_view(),),
    path('create_payment_intent/',CreateCheckoutIntentView.as_view(),),
    path('success/',payment_success),
    path('cancel/',payment_failed),
    path('webhook/',StripeWebhookView.as_view(),),
]
