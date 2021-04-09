from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as django_views

from . import views

app_name = "core"

urlpatterns = [    
    url(r"^$", views.LoginView.as_view(), name="login"),
    url(r"^login/$", views.LoginView.as_view(), name="login"),         
    url(r"^signup/$", views.SignupView.as_view(), name="signup"),    
    url(r"^logout/$", views.AuthSystem.logout, name="logout"),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.AuthSystem.activate, name='activate'),
    
    url(r"^password/reset/$", views.PasswordResetView.as_view(), name="password_reset"),
    url(r"^password/reset/done/$", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    url(r"^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    url(r"^password/reset/done/$", views.PasswordResetCompleteView.as_view(), name="reset_password_complete"),
    url(r"^password/change/$", views.ChangePassword.as_view(), name="change-password"),
    
]
