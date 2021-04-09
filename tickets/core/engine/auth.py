from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.contrib.auth.models import Group

from core.engine import UserAdmin

class Auth(UserAdmin):

    url_login_sucess = 'backoffice:tickets'

    def login_success(self):       
        if self.request.user.is_authenticated:         
            return redirect(reverse(self.url_login_sucess))                      
        else:
            return redirect(reverse("core:login"))


    def logout(self):        
        auth.logout(self)
        return redirect(reverse("core:login"))

    def signup(self, form, dispatcher):        

        next_url = self.request.POST.get("next", "login-success/")

        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        
        user = auth.authenticate(request=self, email=email, password=password)
    

        if user:
            
            user.is_active = False

            group = Group.objects.get(name='Member')
            user.groups.add(group)                

            auth.login(self, user)
            return self.login_success()
        
        else:
            return dispatcher
    
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
            
            return HttpResponse('El link de activación es inválido')
