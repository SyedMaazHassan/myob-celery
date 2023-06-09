from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('myob/login/', views.myob_login, name='myob_login'),
    path('myob/callback/', views.myob_callback, name='myob_callback'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
