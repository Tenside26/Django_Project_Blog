from django.contrib import admin
from .models import CustomUserModel, FriendListModel, FriendModel
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.admin import UserAdmin


class UserModelAdmin(UserAdmin):
    add_form = UserRegisterForm
    form = UserUpdateForm
    model = CustomUserModel
    list_display = ["email", "username"]


admin.site.register(CustomUserModel, UserModelAdmin)


@admin.register(FriendListModel)
class FriendListModelAdmin(admin.ModelAdmin):
    list_display = ["list_owner"]


@admin.register(FriendModel)
class FriendModelAdmin(admin.ModelAdmin):
    list_display = ["friend_list", "friend", "status"]
