from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_view, name="blog"),
    path('post-detail/<str:slug>', views.post_detail_view, name="post-detail"),
    path('create-post', views.create_post_view, name="create-post"),
    path('edit-post/<str:slug>', views.edit_post_view, name="edit-post"),
    path('delete-post/<str:slug>', views.delete_post_view, name="delete-post"),
    path('create-comment/<str:slug>', views.create_post_comment_view, name="create-post-comment"),
    path('edit-comment/<str:slug>/<str:pk>', views.edit_post_comment_view, name="edit-post-comment"),
    path('delete-comment/<str:slug>/<str:pk>', views.delete_post_comment_view, name="delete-post-comment"),
    path('search-results/', views.search_results_view, name="search-results"),
]