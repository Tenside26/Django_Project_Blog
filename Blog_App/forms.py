from django.forms.models import ModelForm
from .models import PostsModel, CommentsModel


class PostModelForm(ModelForm):
    class Meta:
        model = PostsModel
        fields = ["post_title", "post_content", "post_tag"]


class CommentPostForm(ModelForm):
    class Meta:
        model = CommentsModel
        fields = ["com_content"]
