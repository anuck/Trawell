from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'{username} Account has been created. Now you are able to login')
            email_subject = "Email confirmation"
            email_body = 'Thank you for registering to TraWell !! Happy travelling.'
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
                )
            email.fail_silently = False
            email.send()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'Users/register.html',{'form':form})
