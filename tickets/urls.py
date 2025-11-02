from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_ticket, name='submit_ticket'),
    path('success/', views.success, name='success'),
    path('dashboard/', views.ticket_dashboard, name='ticket_dashboard'),
    path("ticket/<int:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    path("ticket/<int:ticket_id>/resolve/", views.resolve_ticket, name="resolve_ticket"),
]
