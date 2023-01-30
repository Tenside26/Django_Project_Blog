from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login_view, name="login"),
    path('register', views.user_register_view, name="register"),
    path('logout', views.user_logout_view, name="logout"),
    path('user-panel/<str:username>', views.user_panel_view, name="user-panel"),
    path('other-user-panel/<str:username>', views.other_user_panel_view, name="other-user-panel"),
    path('user-friend-list/<str:username>', views.user_friend_list_view, name="user-friend-list"),
    path('user-search-friend', views.search_friend_view, name="search-friend"),
    path('user-update/<str:username>', views.user_update_view, name="user-update"),
    path('user-password-change', views.user_password_change_view, name="user-password-change"),
]
