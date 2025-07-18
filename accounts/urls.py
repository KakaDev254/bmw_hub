from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/registration/password_reset_complete.html'), name='password_reset_complete'),

]
