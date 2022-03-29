"""File to define url routes across the project."""

from . import views
from django.urls import path, reverse
from django.conf import settings
from django.conf.urls.static import static
import django

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('search_recipes', views.search_recipes, name='search_recipes'),
    path(
        '<slug:slug>/update',
        views.PostUpdateView.as_view(),
        name='post-update'),
    path(
        '<slug:slug>/delete',
        views.PostDeleteView.as_view(),
        name='post-delete'),
    path(
        'random_recipe',
        views.RandomPostList.as_view(),
        name='random_recipe'),
    path(
        'about',
        django.views.generic.TemplateView.as_view(template_name='about.html'),
        name='about'),
    path('post/new/', views.add_recipe, name='post-create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
