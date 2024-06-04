from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


class CommonLoginView(LoginView):
    template_name = "common/registration/login.html"


class CommonLogoutView(LogoutView):
    template_name = "common/registration/logged_out.html"
