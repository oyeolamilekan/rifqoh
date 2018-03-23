from django.urls import path
from . import views
from django.contrib.auth.views import login,logout,password_change,password_change_done,password_reset,password_reset_done,password_reset_confirm,password_reset_complete

urlpatterns = [
	path('', views.user_login, name='login'),
	path('password-change/',password_change,{'template_name':'registration/password_change_for.html'},name="password_change"),
    path('passowrd-change/done/',password_change_done,{'template_name':'registration/password_change_don.html'},name="password_change_done"),
	path('logout/', logout,{'template_name':'registration/logged_ou.html'}, name='logout'),
	path('stream/', views.stream, name='stream'),
	path('sub/', views.subscribe, name='subscribe'),
	path('register/', views.register, name='register'),
	path('userChoice/',views.userChoice,name='userChoice'),
	path('password-reset/',password_reset,name='password_reset'),
    path('password-reset/done/',password_reset_done,name="password_reset_done"),
    path('password-reset/reset/<uidb64>/<token>/',password_reset_confirm,name="password_reset_confirm"),
    path('password-reset/complete/',password_reset_complete,name="password_reset_complete"),
]