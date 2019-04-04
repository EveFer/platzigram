from django.contrib import admin

from posts.models import Posts
# Register your models here.

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):

    list_display = ('pk', 'profile', 'title', 'photo')