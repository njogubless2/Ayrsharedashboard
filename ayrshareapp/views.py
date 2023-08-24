from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ScheduledPostForm


def scheduled_post(request):
    if request.method == 'POST':
        form = ScheduledPostForm(request.POST)
        if form.is_valid():
            #process the form data and schedule the post
            form.save()
            return redirect('sucess_view') #redirect after successful form submission.
    else:
        form = ScheduledPostForm()
        
    return render(request, 'index.html')
