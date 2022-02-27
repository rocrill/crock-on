from . import views
from django.urls import path, reverse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('success/', views.PostList.as_view(), name='success'),
    path('update_success/', views.PostList.as_view(), name='update_success'),
    path('delete_success/', views.PostList.as_view(), name='delete_success'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('search_recipes', views.search_recipes, name='search_recipes'),
    path('<slug:slug>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('<slug:slug>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    #path('post/new/', views.PostCreateView.as_view(success_url="/success/"), name='post-create'),
    path('post/new/', views.add_recipe, name='post-create'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)