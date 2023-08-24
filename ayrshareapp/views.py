from django.shortcuts import render, redirect
from .forms import ScheduledPostForm
from .models import ScheduledPost
from django.utils import timezone  # You need to import timezone

import requests

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
