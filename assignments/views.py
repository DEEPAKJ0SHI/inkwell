from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Subscriber

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Subscriber.objects.filter(email=email).exists():
            messages.warning(request, 'This email is already subscribed!')
        else:
            Subscriber.objects.create(email=email)
            messages.success(request, 'Thank you for subscribing!')
    return redirect(request.META.get('HTTP_REFERER', '/'))

