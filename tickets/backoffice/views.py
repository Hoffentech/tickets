from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View, FormView
from django.db.models import Avg, Count, Min, Sum, F, Q, Value, Case, When, CharField, Subquery, OuterRef, Prefetch, Func
from django.db.models.functions import TruncDate, TruncTime, Concat

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from core.models import User
from backend.models import *
from backoffice.forms import TicketForm

#----------------------------------------------------------------------------------/*
# | TICKETS VIEWS
#----------------------------------------------------------------------------------/*

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='../login/'), name='dispatch')
class TicketsListView(ListView):
    # Listado de tickets
    model = Ticket
    template_name = 'backoffice/tickets/index.html'
    context_object_name = 'tickets'

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='../login/'), name='dispatch')
class TicketCreateView(CreateView):
    # Crear un nuevo ticket
    model = Ticket
    form_class = TicketForm
    template_name = 'backoffice/tickets/create.html'
    context_object_name = 'ticket'    
    success_url = reverse_lazy('backoffice:tickets')  

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='../login/'), name='dispatch')
class TicketUpdateView(UpdateView):
    # Actualizar un nuevo ticket
    model = Ticket
    form_class = TicketForm
    template_name = 'backoffice/tickets/update.html'
    context_object_name = 'ticket'      
    success_url = reverse_lazy('backoffice:tickets')