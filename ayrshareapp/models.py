from django.db import models


class CLient (models.Model):
    name= models.CharField(max_length=200)
    email= models.EmailField(max_length=255)
    password= models.CharField(max_length=150)


class SocialMediaPlatform (models.Model):
    name= models.CharField(max_length=50)
    ayrshare_api_key=models.CharField(max_length=100)
    ayrshare_api_secret=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class ScheduledPost(models.Model):
    content = models.TextField()
    Scheduled_datetime=models.DateTimeField()
    social_media_platform=models.ForeignKey(social_media_platform, on_delete=models.CASCADE)
    is_published=models.BooleanField(default=False)
    
    def __str__(self):
        return f"Post '{self.content[:20]}..' scheduled for{self.Scheduled_datetime} on { self.social_media_platform}"
    