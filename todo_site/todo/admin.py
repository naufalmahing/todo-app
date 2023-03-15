from django.contrib import admin
from .models import Tag, Todo

# class TagInline(admin.TabularInline):
#     model = Todo.tags.through
#     extra = 3

# class TodoAdmin(admin.ModelAdmin):
#     fields = ['todo_title', 'text']
#     inlines = [TagInline]
#     list_filter = ['tags']
#     search_fields = ['todo_title']

# admin.site.register(Todo, TodoAdmin)
admin.site.register(Todo)
admin.site.register(Tag)