from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('template/', views.base_template, name='template'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.LogoutView.as_view(), name='signout'),
]