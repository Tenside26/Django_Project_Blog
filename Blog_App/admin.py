from django.contrib import admin
from .models import PostsModel, CommentsModel, PostVotesModel, CommentVotesModel, ViewsModel, TagsModel


@admin.register(PostsModel)
class PostsModelAdmin(admin.ModelAdmin):
    list_display = ["post_title", "post_user"]


@admin.register(CommentsModel)
class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ["com_user"]


@admin.register(PostVotesModel)
class PostVotesModelAdmin(admin.ModelAdmin):
    list_display = ["vote_post_user", "vote_post_rating"]


@admin.register(CommentVotesModel)
class CommentVotesModelAdmin(admin.ModelAdmin):
    list_display = ["vote_com_user", "vote_com_rating"]


@admin.register(ViewsModel)
class ViewsModelAdmin(admin.ModelAdmin):
    list_display = ["view_user", "view_post"]


@admin.register(TagsModel)
class TagsModelAdmin(admin.ModelAdmin):
    list_display = ["tag"]
