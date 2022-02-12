from . import views
from django.urls import path

url patterns = [
    path('', views.PostList.as_view(), name='home')
]