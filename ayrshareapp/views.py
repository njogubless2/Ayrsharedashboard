from django.shortcuts import render, redirect
from django.forms import ScheduledPostForm
from .models import ScheduledPost
from django.utils import timezone 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import requests

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to the user's dashboard page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Implement a similar view for user login


@login_required
def dashboard(request):
    user = request.user
    scheduled_posts = ScheduledPost.objects.filter(user=user)  # Assuming you add a 'user' field to the ScheduledPost model
    return render(request, 'dashboard.html', {'scheduled_posts': scheduled_posts})


def perform_api_integration(content, scheduled_datetime):
    api_url = "https://api.example.com"  # Replace with your actual API URL
    headers = {
        "Authorization": "Bearer YOUR_API_TOKEN"  # Replace with your actual API token
    }
    data = {
        "text": content,
        "scheduled_at": scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    response = requests.post(api_url, json=data, headers=headers)
    return response.status_code == 200

def schedule_post(request):
    if request.method == 'POST':
        form = ScheduledPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            scheduled_datetime = form.cleaned_data['scheduled_datetime']
            
            if scheduled_datetime <= timezone.now():
                form.add_error('scheduled_datetime', "Scheduled time must be in the future.")
                return render(request, 'schedule_post.html', {'form': form})
            
            scheduled_post = form.save(commit=False)
            if perform_api_integration(content, scheduled_datetime):
                scheduled_post.is_published = True
                scheduled_post.save()
                return redirect('success_view')  # Replace with your success view name
            else:
                # Handle API integration error
                pass  # You might want to add some error handling logic here
    else:
        form = ScheduledPostForm()
    
    return render(request, 'schedule_post.html', {'form': form})
