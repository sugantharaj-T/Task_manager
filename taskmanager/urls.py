from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from core.forms import EmailOrUsernameAuthenticationForm
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html", authentication_form=EmailOrUsernameAuthenticationForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="auth/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"), name="password_reset_done"),
    path("register/", views.register, name="register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
