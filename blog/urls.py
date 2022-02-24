from . import views
from django.urls import path, reverse

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('success/', views.PostList.as_view(), name='success'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('search_recipes', views.search_recipes, name='search_recipes'),
    path('post/new/', views.PostCreateView.as_view(success_url="/success/"), name='post-create'),
]