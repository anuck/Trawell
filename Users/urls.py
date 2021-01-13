from django.urls import path, include
from . import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',user_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),

    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="Users/password_reset.html"),
        name="reset_password",),
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="Users/password_reset_sent.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="Users/password_reset_form.html"),
        name="password_reset_confirm"),
    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="Users/password_reset_done.html"),
        name="password_reset_complete"),


]


