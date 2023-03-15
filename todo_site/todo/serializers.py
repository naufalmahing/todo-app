from .models import Todo, Tag
from django.contrib.auth.models import User
from rest_framework import serializers

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Todo
        fields = ['url', 'id', 'todo_title', 'tags', 'text', 'owner']
        extra_kwargs = {
            'url': {'view_name': 'todo:todo-detail'},
            'tags': {'view_name': 'todo:tag-detail'},
        }

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'id', 'tag_title', 'todo_set']
        extra_kwargs = {
            'url': {'view_name': 'todo:tag-detail'},
            'todo_set': {'view_name': 'todo:todo-detail'},
        }

class UserSerializer(serializers.HyperlinkedModelSerializer):
    todo_set = serializers.HyperlinkedRelatedField(many=True, view_name='todo:todo-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'todo_set']
        extra_kwargs = {
            'url': {'view_name': 'todo:user-detail'},
        }