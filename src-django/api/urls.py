from django.urls import path
from .views import email_confirmed_view

urlpatterns = [
    path('email-confirmed/', email_confirmed_view),
]