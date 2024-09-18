from django.urls import path
from authentication.views import RegisterView, LoginView, KYCView, WebhookView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(), name='login'),
    path('kyc/',KYCView.as_view(),name = 'kyc_form'),
    path('webhook/',WebhookView.as_view(),name = 'webhook'),

]