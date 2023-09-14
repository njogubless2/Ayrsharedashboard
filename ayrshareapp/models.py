from django.db import models
from django.contrib.auth.models import User  # You may need to adjust the user model if you have a custom user model

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    social_media_platforms = models.ManyToManyField('SocialMediaPlatform')

    def __str__(self):
        return self.user.username

# Social Media Platform Model
class SocialMediaPlatform(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='platform_icons/')

    def __str__(self):
        return self.name

# Content Model
class Content(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content_text = models.TextField()
    image = models.ImageField(upload_to='content_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Scheduled Post Model
class ScheduledPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    platform = models.ForeignKey(SocialMediaPlatform, on_delete=models.CASCADE)
    scheduled_datetime = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"Scheduled Post by{self.user.username} at {self.scheduled_datetime}"

# Analytics Model
class PostAnalytics(models.Model):
    scheduled_post = models.ForeignKey(ScheduledPost, on_delete=models.CASCADE)
    views = models.PositiveIntegerField()
    likes = models.PositiveIntegerField()
    comments = models.PositiveIntegerField()

    def __str__(self):
        return f"Analytics for {self.scheduled_post}"
