from django.urls import path
from . import views

urlpatterns = [
    path('', views.sync_home_view, name='sync'),
    # path('myob/login/', views.myob_login, name='myob_login'),
    # path('myob/callback/', views.myob_callback, name='myob_callback'),
]
