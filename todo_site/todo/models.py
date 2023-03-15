from django.db import models
from django import forms
from django.contrib.auth.models import User

class Tag(models.Model):
    tag_title = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_title

class Todo(models.Model):
    todo_title = models.CharField(max_length=200)
    text = models.TextField(max_length=1000, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.todo_title

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo_title', 'tags', 'text']
    

class UploadFileForm(forms.Form):
    file = forms.FileField()