from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from .forms import CustomAuthenticationForm
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     redirect_authenticated_user=True,
                                     extra_context={'title': 'Авторизация'},
                                     form_class=CustomAuthenticationForm),
         name='login'),
    path('registration/', RegisterCustomUser.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(template_name='users/password_change.html'),
         name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),


    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html',
                                                      email_template_name='users/password_reset_email.html'),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
