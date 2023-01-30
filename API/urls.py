from django.urls import path
from . import views

urlpatterns = [
    path('posts_list/', views.api_posts_list_view),
    path('posts_detail/<str:pk>/', views.api_post_detail_view),
]