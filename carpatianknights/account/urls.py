from django.urls import path, include
from django.contrib.auth import views as auth_views
from carpatianknights.account import views


# app_name = 'account'

urlpatterns = [
    #     path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #     path('registration_to_tour/', views.registration_to_tour, name='registration_to_tour'),
    path('', views.dashboard, name='dashboard'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # Обработчики восстановления пароля.
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
