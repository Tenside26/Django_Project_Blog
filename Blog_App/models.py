
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


VOTES = [
        ('Like', 'Like'),
        ('Dislike', 'Dislike')
    ]


class TagsModel(models.Model):

    tag = models.CharField(max_length=80)

    def __str__(self):
        return self.tag


class PostsModel(models.Model):

    post_title = models.CharField(max_length=80)
    post_slug = models.SlugField(max_length=80, null=True, blank=True)
    post_picture = models.ImageField(blank=True)
    post_content = models.TextField(max_length=1000)
    post_date_created = models.DateTimeField(auto_now_add=True)
    post_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_post")
    post_tag = models.ManyToManyField(TagsModel, blank=True, related_name="post_tag")

    def save(self, *args, **kwargs):
        self.post_slug = slugify(self.post_title)
        super(PostsModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.post_slug)])

    def __str__(self):
        return self.post_title


class CommentsModel(models.Model):

    com_content = models.TextField(max_length=1000)
    com_date_created = models.DateTimeField(auto_now_add=True)
    com_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comment")
    com_post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, related_name="com_post", null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class PostVotesModel(models.Model):
    vote_post_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vote_post_user")
    vote_post_date_created = models.DateTimeField(auto_now_add=True)
    vote_post_rating = models.CharField(max_length=10, choices=VOTES)
    vote_post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, related_name="vote_post", null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    def post_if_like(self):
        if self.vote_post_rating == 'Like':
            return True

    def post_if_dislike(self):
        if self.vote_post_rating == 'Dislike':
            return True


class CommentVotesModel(models.Model):
    vote_com_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vote_com_user")
    vote_com_date_created = models.DateTimeField(auto_now_add=True)
    vote_com_rating = models.CharField(max_length=10, choices=VOTES)
    vote_comment = models.ForeignKey(CommentsModel, on_delete=models.CASCADE, related_name="vote_comment")

    def __str__(self):
        return str(self.pk)

    def comment_if_like(self):
        if self.vote_com_rating == 'Like':
            return True

    def comment_if_dislike(self):
        if self.vote_com_rating == 'Dislike':
            return True


class ViewsModel(models.Model):
    view_user = models.CharField(max_length=80)
    view_post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, related_name="view_post", null=True, blank=True)
