from django.contrib.auth import mixins
from .permissions import IsOwner
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import TodoSerializer, UserSerializer, TagSerializer
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Todo, Tag, TodoForm, UploadFileForm
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy

class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'todo/index.html'
    context_object_name = 'data'
    login_url = 'accounts:signin'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Todo.objects.filter(owner=self.request.user)

class DetailView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DetailView):
    model = Todo
    template_name = 'todo/detail.html'
    context_object_name = 'data'

    def test_func(self):
        return self.request.user.username == self.get_object().owner.username

class NewTodoView(generic.CreateView):
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy('todo:index')
    template_name = 'todo/create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class UpdateTodoView(generic.UpdateView):
    model = Todo
    form_class = TodoForm
    success_url = 'todo:detail'
    template_name = 'todo/update.html'

    def get_success_url(self):
        todo = self.get_object()
        return reverse_lazy(self.success_url, args=(todo.id,))

class DeleteTodoView(generic.DeleteView):
    model = Todo
    success_url = reverse_lazy('todo:index')
    template_name = 'todo/index.html'

class UploadView(generic.View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            self.handle_file_uploaded(request.FILES['file'])
            messages.success(request, 'Berhasil import')
            return HttpResponseRedirect(reverse_lazy('todo:index'))
        return render(request, 'todo/upload.html', {
            'upload_form': form
        })

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'todo/upload.html', {
            'upload_form': form
        })

    def handle_file_uploaded(self, file):
        for chunk in file.chunks():
            [Todo.objects.create(todo_title=e, owner=self.request.user) for e in chunk.decode().split('\n')]

class TodoList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [
        IsOwner,
    ]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(username=self.request.user.username)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]

class TagDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('todo:user-list', request=request, format=format),
        'todos': reverse('todo:todo-list', request=request, format=format),
    })

@api_view(['GET'])
def index_template(request):
    return render(request, 'todo/base.html')