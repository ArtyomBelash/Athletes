from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import *


class RegisterCustomUser(SuccessMessageMixin, CreateView):
    form_class = CustomRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

    # def get_success_message(self, cleaned_data):
    #     sm = f'{cleaned_data["username"]}, прошлі рег'
    #     return sm
