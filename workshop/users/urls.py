
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'users'

urlpatterns = [
    path('register-login/', views.RegisterLoginView.as_view(), name='register_login'),
    path('profile/', views.user_profile, name ='user_profile'),
    path('logout/', LogoutView.as_view(next_page='bboard:index') ,name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset', PasswordResetView.as_view(), name ='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name ='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name ='password_reset_complete'),
     ]