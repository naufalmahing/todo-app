from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views
from django.urls import reverse_lazy, reverse

class SignupView(generic.CreateView):
    model = User
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('todo:index')

class SigninView(views.LoginView):
    template_name = 'accounts/signin.html'
    redirect_authenticated_user = 'todo:index'

class LogoutView(views.LogoutView):
    template_name = 'todo/index.html'

def base_template(request):
    return render(request, 'accounts/base.html')