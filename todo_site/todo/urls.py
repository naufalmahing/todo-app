from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'todo'
urlpatterns = [
    path('template/', views.index_template, name='index-template'),
    path('api/', views.api_root, name='root'),
    path('api/todo/', views.TodoList.as_view(), name='todo-list'),
    path('api/todo/<int:pk>/', views.TodoDetail.as_view(), name='todo-detail'),
    path('api/tag/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
    path('api/user/', views.UserList.as_view(), name='user-list'),
    path('api/user/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('create/', views.NewTodoView.as_view(), name='create'),
    path('update/<int:pk>/', views.UpdateTodoView.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteTodoView.as_view(), name='delete'),
    path('upload/', views.UploadView.as_view(), name='upload'),
]

urlpatterns = format_suffix_patterns(urlpatterns)