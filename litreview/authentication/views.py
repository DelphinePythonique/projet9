# authentication/views.py
from django.conf import settings
from django.contrib.auth import  login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render



"""
def logout_user(request):
    logout(request)
    return redirect('login')
"""

def signup_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})