
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_color = models.CharField(max_length=7, default='#FF4500')
    bio = models.TextField(blank=True, max_length=200)
    karma = models.IntegerField(default=0)
    cake_day = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Forum(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='forums_created')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'r/{self.name}'

    class Meta:
        ordering = ['name']


class Post(models.Model):

    POST_TYPE_CHOICES = [
        ('text', 'Text'),
        ('link', 'Link'),
        ('image', 'Image'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('removed', 'Removed'),
        ('archived', 'Archived'),
    ]

    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    title = models.CharField(max_length=300)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='text')
    body = models.TextField(blank=True)
    url = models.URLField(blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def score(self):
        return self.upvotes - self.downvotes

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('removed', 'Removed'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    body = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

    @property
    def score(self):
        return self.upvotes - self.downvotes

    class Meta:
        ordering = ['created_at']