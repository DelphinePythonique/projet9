from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from . import views

app_name = "authentication"
urlpatterns = [
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", views.signup_page, name="signup"),
    path("follow/", views.follow_user, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow_user, name="unfollow"),
]
