from django.urls import path
from . import views
from django.contrib.auth.views import login, logout, logout_then_login
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', login, name='login'),
    path('logout/', logout, {'next_page': '/account/post-logout'}, name='logout'),
    path('post-logout/', views.user_logout, name='post-logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),
    path('', views.dashboard, name='dashboard'),

    path('password-change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password-change/done', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('register/', views.register, name='register'),
]
