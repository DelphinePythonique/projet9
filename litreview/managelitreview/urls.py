from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from . import views

app_name = 'managelitreview'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('tickets/new', views.create_ticket, name='create_ticket'),
    path('tickets/reviews/new', views.create_review, name='create_review'),
    path('tickets/<int:ticket_id>/edit', views.update_ticket, name='update_ticket'),
    path('tickets/<int:ticket_id>/delete', views.delete_ticket, name='delete_ticket'),
    path('tickets/<int:ticket_id>', views.display_ticket, name='display_ticket'),
    path('mytickets/', views.display_my_tickets, name='display_my_tickets'),
]