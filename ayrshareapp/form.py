from django import forms
from .models import ScheduledPost


class ScheduledPost(forms.Modelform):
    class Meta:
        model = ScheduledPost
        fields = ['content','scheduled_datetime', 'social_media_platform']
