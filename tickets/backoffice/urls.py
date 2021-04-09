from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as django_views

from . import views
app_name = "backoffice"

urlpatterns = [    

    # Tickets    
    path("tickets", views.TicketsListView.as_view(), name="tickets"),
    path("ticket/create", views.TicketCreateView.as_view(), name="ticket-create"),
    path("ticket/<int:pk>/update", views.TicketUpdateView.as_view(), name="ticket-update"),

]