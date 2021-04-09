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
    path("ticket/<int:pk>/detalle", views.TicketDetailView.as_view(), name="ticket"),     

   # Users
    path("users", views.UsersListView.as_view(), name="users"),
    path("user/create", views.UserCreateView.as_view(), name="user-create"),
    path("user/<int:pk>/update", views.UserUpdateView.as_view(), name="user-update"),    


]
