# authentication/views.py
from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.shortcuts import redirect, render
from .forms import SignupForm, SearchUserForm
from .models import UserFollows

"""
def logout_user(request):
    logout(request)
    return redirect('login')
"""


def signup_page(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", context={"form": form})


def follow_user(request):
    form = SearchUserForm()
    followed = UserFollows.objects.filter(
                user=request.user
            )
    followers = UserFollows.objects.filter(
        followed_user=request.user
    )
    if request.method == "POST":
        form = SearchUserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            followed_user = get_user_model().objects.filter(
                username=cleaned_data["username"]
            )
            if len(followed_user) > 0:
                try:
                    link = UserFollows(
                        user=request.user, followed_user=followed_user[0]
                    )
                    link.save()
                except IntegrityError:
                    pass

            return redirect("authentication:follow")
    else:
        form = SearchUserForm()
    return render(request, "authentication/follow.html",
                  {
                      "form": form,
                      "followed": followed,
                      "followers": followers,
                  })
