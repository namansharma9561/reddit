
from django.contrib import admin
from .models import UserProfile, Forum, Post, Comment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'karma', 'cake_day']
    search_fields = ['user__username', 'user__email']


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'forum', 'author', 'post_type', 'score', 'status', 'is_pinned', 'created_at']
    list_filter = ['post_type', 'status', 'is_pinned', 'forum', 'created_at']
    search_fields = ['title', 'body', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'score']
    list_editable = ['status', 'is_pinned']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'post', 'author', 'score', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['body', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at', 'score']
    list_editable = ['status']