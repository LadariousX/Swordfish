from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_ticket, name='submit_ticket'),
    path('success/', views.success, name='success'),
]
