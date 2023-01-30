from rest_framework import serializers
from Blog_App.models import PostsModel, CommentsModel


class PostsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostsModel
        fields = ["post_title", "post_slug", "post_content", "post_date_created", "post_user", "post_tag"]


class CommentsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsModel
        fields = ["com_content", "com_date_created", "com_user", "com_post"]
