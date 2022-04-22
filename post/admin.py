from django.contrib import admin
from .models import Author, Post, Subscriber, Category,Comment

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Subscriber)
admin.site.register(Category)
admin.site.register(Comment)
