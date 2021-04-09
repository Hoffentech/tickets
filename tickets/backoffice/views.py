from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View, FormView
from django.db.models import Avg, Count, Min, Sum, F, Q, Value, Case, When, CharField, Subquery, OuterRef, Prefetch, Func
from django.db.models.functions import TruncDate, TruncTime, Concat

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy

from core.models import User
from backend.models import *
from backoffice.forms import TicketForm, UserForm

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
class TicketDetailView(DetailView):
    # Detalle de ticket
    model = Ticket
    template_name = 'backoffice/tickets/detail.html'
    context_object_name = 'ticket'

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='../login/'), name='dispatch')
class TicketCreateView(CreateView):
    # Crear un nuevo ticket
    model = Ticket
    form_class = TicketForm
    template_name = 'backoffice/tickets/create.html'
    context_object_name = 'ticket'    
    success_url = reverse_lazy('backoffice:tickets')  

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='../login/'), name='dispatch')
class TicketUpdateView(UpdateView):
    # Actualizar un nuevo ticket
    model = Ticket
    form_class = TicketForm
    template_name = 'backoffice/tickets/update.html'
    context_object_name = 'ticket'      
    success_url = reverse_lazy('backoffice:tickets')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw    


#----------------------------------------------------------------------------------/*
# | USERS VIEW
#----------------------------------------------------------------------------------/*        

@method_decorator(login_required(login_url='../login/'), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser),name='dispatch')
class UsersListView(ListView):
    """View users """    
    model = User
    template_name = "backoffice/user/index.html"
    context_object_name = 'users'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context          

@method_decorator(login_required(login_url='../login/'), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser),name='dispatch')
class UserCreateView(CreateView):
    """Create member """
    model = User
    form_class = UserForm
    template_name = "backoffice/user/create.html"
    success_url = reverse_lazy('backoffice:users')
    context_object_name = 'user'       

    def form_valid(self, form):
        try:

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            tax_number = form.cleaned_data['tax_number']
            name = '{0} {1}'.format(first_name, last_name)

            email = form.cleaned_data['email']

            user = User.objects.create(email=email, name=name)
            user.groups.set('2')
            password = "{0}{1}{2}".format(first_name[0],last_name[0], tax_number)
            user.set_password(password)
            user.save()              
            
        except Exception as e:
            raise e        
        return super().form_valid(form)                            

@method_decorator(login_required(login_url='../login/'), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser),name='dispatch')
class UserUpdateView(UpdateView):
    """Update user """
    model = User
    form_class = UserForm
    template_name = "backoffice/user/update.html"
    success_url = reverse_lazy('backoffice:users')
    context_object_name = 'user'