import os
import urllib.request
from django.http import HttpResponse
from urllib.parse import urlparse

from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.contrib.auth.models import Group
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError, Http404,
)
from django.contrib.sites.shortcuts import get_current_site
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View, FormView
from django.contrib.auth import views as django_views
from django.contrib.auth import login as dj_login
from django.template.response import TemplateResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.shortcuts import render

from core.tokens import account_activation_token
from core.models import User
from core.forms import (
    LoginForm,
    SignupForm,
    UserForm,
    PasswordResetForm,
    PasswordResetConfirmForm,
    ChangePasswordForm
)

from core.engine import Auth

class CoreDashboard(TemplateView):
    template_name = "core/index.html"

#----------------------------------------------------------------------------------/*
# | AUTH VIEW 
#----------------------------------------------------------------------------------/*        

class AuthSystem:

    @login_required
    def login_success(self):

        if self.user.is_authenticated:

            if self.user.groups.filter(name__in=['HIT']).exists():
                return redirect(reverse('core:dashboard'))

            elif self.user.groups.filter(name__in=['Member']).exists():            
                return redirect(reverse('operations:portal-bookings'))            

            elif self.user.groups.filter(name__in=['Supplier']).exists():            
                return redirect(reverse('suppliers:portal-suppliers-profile'))

            else:            
                return redirect(reverse('core:dashboard'))                      

        else:
            return HttpResponseForbidden()

    def google_login(self):

        try:
            if not self.POST.get('idtoken'):
                return HttpResponse({'error': 'Missing code'}, status=400)

            token = self.POST.get('idtoken')

            CLIENT_ID_HOFFENTECH = os.getenv(
                'GOOGLE_CLIENT_ID_HOFFENTECH', None)
            CLIENT_ID_HIT = os.getenv('GOOGLE_CLIENT_ID_HIT', None)

            idinfo = id_token.verify_oauth2_token(token, requests.Request())

            if idinfo['aud'] not in [CLIENT_ID_HOFFENTECH, CLIENT_ID_HIT]:
                return HttpResponse({'Audience not verify'}, status=500)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return HttpResponse({'Wront issuer'}, status=500)

            user = User.objects.filter(email=idinfo['email']).first()

            if user and not user.is_active:
                return HttpResponse({'error': 'Auth failed, user is not active.'}, status=401)

            if user is not None:
                dj_login(self, user)
            else:
                return HttpResponse({'error': 'Auth failed, user is not active.'}, status=401)

            if self.user.is_authenticated:
                return HttpResponse(status=200)
            else:
                return HttpResponse(e, status=500)

        except ValueError as e:
            return HttpResponse(e, status=500)

    @login_required
    def logout(self):
        # Logout user from Django AuthSystem
        auth.logout(self)
        return redirect(reverse("core:login"))

    def signup(self):
        # SingUp new user

        form = SignupForm(self.POST or None)
        next_url = self.GET.get("next", "login-success/")

        if form.is_valid():
            form.save()

            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            user = auth.authenticate(request=self, email=email, password=password)
            user.is_active = False

            group = Group.objects.get(name='Supplier')
            user.groups.add(group)
            
            notificacion_activation_email.delay(user.id)

            if user:
                auth.login(self, user)

            redirect_url = self.POST.get("next", "login-success/")

            return redirect(redirect_url)

        ctx = {"form": form, "next": next_url}

        return TemplateResponse(self, "registration/signup.html", ctx)

    def signup_supplier(self):
        # SingUp new user

        form = SignupForm(self.POST or None)
        next_url = self.GET.get("next", "login-success/")

        if form.is_valid():
            form.save()

            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            user = auth.authenticate(request=self, email=email, password=password)
            
            # Add to suppliers group
            group = Group.objects.get(name='Supplier')
            user.groups.add(group)
            
            # Send activation email
            user.is_active = False
            notificacion_activation_email.delay(user.id)
            
            # Login user
            if user:
                auth.login(self, user)

            # Redirect to portal
            redirect_url = self.POST.get("next", "/login-success/")
            return redirect(redirect_url)

        ctx = {"form": form, "next": next_url}
        return TemplateResponse(self, "registration/signup_supplier.html", ctx)           

    def activate(self, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            auth.login(self, user)
            return redirect(reverse('suppliers:portal-suppliers-profile'))
        else:
            return HttpResponse('Link de activación es inválido')

class LoginView(Auth, django_views.LoginView):
    template_name="registration/login.html"    
    authentication_form=LoginForm
 
    def form_valid(self, form):      
        super().form_valid(form)
        return self.login_success()        

class SignupView(Auth, CreateView):
    template_name="registration/signup.html"
    form_class=SignupForm
    success_url= reverse_lazy('core:login')

    def form_valid(self, form):
        return self.signup(form, super().form_valid(form))

    def get_initial(self):
        initial = super().get_initial()
        initial['next'] = self.request.GET.get("next", "login-success/")
        return initial 

class ChangePassword(View):

    def get(self, request):
        form = ChangePasswordForm(initial={'username': self.request.GET.get('user')})    
        return render(request, 'registration/change_password.html', {'form': form})

    def post(self, request):
        try:
            username=self.request.POST.get('username', None)
            password=self.request.POST.get('password', None)
            u = User.objects.get(email=username)
            u.set_password(password)
            u.save()
            return HttpResponse('Contraseña modificada con éxito')            
        except Exception as e:
            print(e)
            return HttpResponse('Ocurrió un error')

class PasswordResetView(django_views.PasswordResetView):
    template_name = "registration/password_reset_form.html"
    form_class = PasswordResetForm
    success_url= reverse_lazy('core:password_reset_done')
    
class PasswordResetDoneView(django_views.PasswordResetDoneView):    
    template_name = "registration/password_reset_done.html"

class PasswordResetConfirmView(django_views.PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    form_class = PasswordResetConfirmForm
    success_url= reverse_lazy('core:reset_password_complete')

class PasswordResetCompleteView(django_views.PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"