from django.shortcuts import render, redirect
from .models import PostsModel, PostVotesModel, CommentVotesModel, CommentsModel, ViewsModel
from .forms import PostModelForm, CommentPostForm
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="login")
def blog_view(request):

    template = "blog.html"
    like_filter = Q(vote_post__vote_post_rating='Like')
    dislike_filter = Q(vote_post__vote_post_rating='Dislike')
    queryset = PostsModel.objects.annotate(post_views_count=Count("view_post", distinct=True),
                                           post_comments_count=Count("com_post", distinct=True),
                                           post_likes_count=Count("vote_post__vote_post_user", like_filter, distinct=True),
                                           post_dislikes_count=Count("vote_post__vote_post_user", dislike_filter, distinct=True))

    session_data = request.session.get("recently_viewed_posts")
    recently_viewed_posts = None

    if session_data is not None:
        recently_viewed_posts = PostsModel.objects.filter(post_slug__in=session_data)

    if request.method == "POST" and "for_sorting":
        if "post_date_rising" in request.POST["sort"]:
            queryset = queryset.order_by("-post_date_created")

        if "post_date_decreasing" in request.POST["sort"]:
            queryset = queryset.order_by("post_date_created")

        if "views_rising" in request.POST["sort"]:
            queryset = queryset.order_by("-post_views_count")

        if "views_decreasing" in request.POST["sort"]:
            queryset = queryset.order_by("post_views_count")

        if "like_rising" in request.POST["sort"]:
            queryset = queryset.order_by("-post_likes_count")

        if "like_decreasing" in request.POST["sort"]:
            queryset = queryset.order_by("post_likes_count")

        if "dislike_rising" in request.POST["sort"]:
            queryset = queryset.order_by("-post_dislikes_count")

        if "dislike_decreasing" in request.POST["sort"]:
            queryset = queryset.order_by("post_dislikes_count")

        if "comments_rising" in request.POST["sort"]:
            queryset = queryset.order_by("-post_comments_count")

        if "comments_decreasing" in request.POST["sort"]:
            queryset = queryset.order_by("post_comments_count")

    return render(request, template, {"queryset": queryset,
                                      "recently_viewed_posts": recently_viewed_posts})


@login_required(login_url="login")
def post_detail_view(request, slug):
    # Fix Like/Dislike Not Disappearing In Post Detail/Comments
    template = "post-detail.html"
    post_like_filter = Q(vote_post__vote_post_rating='Like')
    post_dislike_filter = Q(vote_post__vote_post_rating='Dislike')
    comment_like_filter = Q(vote_comment__vote_com_rating='Like')
    comment_dislike_filter = Q(vote_comment__vote_com_rating='Dislike')

    queryset = PostsModel.objects.annotate(post_views_count=Count("view_post", distinct=True),
                                           post_comments_count=Count("com_post", distinct=True),
                                           post_likes_count=Count("vote_post__vote_post_user", post_like_filter, distinct=True),
                                           post_dislikes_count=Count("vote_post__vote_post_user", post_dislike_filter, distinct=True)).get(post_slug=slug)

    comments = CommentsModel.objects.filter(com_post=queryset).annotate(comment_likes_count=Count("vote_comment__vote_com_user", comment_like_filter, distinct=True),
                                                                        comment_dislikes_count=Count("vote_comment__vote_com_user", comment_dislike_filter, distinct=True))

    if "recently_viewed_posts" in request.session:
        if slug in request.session["recently_viewed_posts"]:
            request.session["recently_viewed_posts"].remove(slug)

        request.session["recently_viewed_posts"].insert(0, slug)
        if len(request.session["recently_viewed_posts"]) > 3:
            request.session["recently_viewed_posts"].pop()
    else:
        request.session["recently_viewed_posts"] = [slug]

    request.session.modified = True

    if not queryset.view_post.filter(view_user=request.user):
        ViewsModel.objects.create(view_user=request.user, view_post=queryset)

    if request.method == "POST":
        if "post_like" in request.POST:
            PostVotesModel.objects.create(vote_post_user=request.user, vote_post_rating="Like", vote_post=queryset)
            messages.add_message(request, messages.SUCCESS, 'You Successfully Liked Post')
            return redirect(queryset)

        if "post_dislike" in request.POST:
            PostVotesModel.objects.create(vote_post_user=request.user, vote_post_rating="Dislike", vote_post=queryset)
            messages.add_message(request, messages.SUCCESS, 'You Successfully Disliked Post')
            return redirect(queryset)

        if "post_unlike" in request.POST:
            vote = PostVotesModel.objects.get(vote_post_user=request.user, vote_post_rating="Like", vote_post=queryset)
            vote.delete()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Unliked Post')
            return redirect(queryset)

        if "post_un-dislike" in request.POST:
            vote = PostVotesModel.objects.get(vote_post_user=request.user, vote_post_rating="Dislike", vote_post=queryset)
            vote.delete()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Un-Dislike Post')
            return redirect(queryset)

        if "com_like" in request.POST:
            comment_id = CommentsModel.objects.get(id=request.POST["pk"])
            CommentVotesModel.objects.create(vote_com_user=request.user, vote_com_rating="Like", vote_comment=comment_id)
            messages.add_message(request, messages.SUCCESS, 'You Successfully Liked Comment')
            return redirect(queryset)

        if "com_dislike" in request.POST:
            comment_id = CommentsModel.objects.get(id=request.POST["pk"])
            CommentVotesModel.objects.create(vote_com_user=request.user, vote_com_rating="Dislike", vote_comment=comment_id)
            messages.add_message(request, messages.SUCCESS, 'You Successfully Disliked Comment')
            return redirect(queryset)

        if "com_unlike" in request.POST:
            comment_id = CommentsModel.objects.get(id=request.POST["pk"])
            vote = CommentVotesModel.objects.get(vote_com_user=request.user, vote_com_rating="Like", vote_comment=comment_id)
            vote.delete()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Unliked Comment')
            return redirect(queryset)

        if "com_un-dislike" in request.POST:
            comment_id = CommentsModel.objects.get(id=request.POST["pk"])
            vote = CommentVotesModel.objects.get(vote_com_user=request.user, vote_com_rating="Dislike", vote_comment=comment_id)
            vote.delete()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Un-Dislike Comment')
            return redirect(queryset)

    return render(request, template, {"queryset": queryset,
                                      "comments": comments})


@login_required(login_url="login")
def create_post_view(request):

    template = "create-post.html"
    form = PostModelForm()

    if request.method == "POST":
        form = PostModelForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.post_user = request.user
            new_form.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Created Post')
            return redirect("blog")

    return render(request, template, {"form": form})


@login_required(login_url="login")
def edit_post_view(request, slug):

    template = "edit-post.html"
    queryset = PostsModel.objects.get(post_slug=slug)
    form = PostModelForm(instance=queryset)

    if request.method == "POST":
        form = PostModelForm(request.POST, instance=queryset)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Edited Post')
            return redirect("blog")

    return render(request, template, {"form": form})


@login_required(login_url="login")
def delete_post_view(request, slug):

    template = "delete-post.html"
    queryset = PostsModel.objects.get(post_slug=slug)

    if request.method == "POST":
        queryset.delete()
        messages.add_message(request, messages.SUCCESS, 'You Successfully Deleted Post')
        return redirect("blog")

    return render(request, template)


@login_required(login_url="login")
def create_post_comment_view(request, slug):

    template = "create-post-comment.html"
    form = CommentPostForm()
    queryset = PostsModel.objects.get(post_slug=slug)

    if request.method == "POST":
        form = CommentPostForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.com_user = request.user
            new_form.com_post = queryset
            new_form.save()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Posted Comment')
            return redirect(queryset)

    return render(request, template, {"form": form,
                                      "queryset": queryset})


@login_required(login_url="login")
def edit_post_comment_view(request, slug, pk):

    template = "edit-post-comment.html"
    queryset = PostsModel.objects.get(post_slug=slug)
    comment = queryset.com_post.get(id=pk)
    form = CommentPostForm(instance=comment)

    if request.method == "POST":
        form = CommentPostForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Edited Comment')
            return redirect(queryset)

    return render(request, template, {"form": form,
                                      "queryset": queryset})


@login_required(login_url="login")
def delete_post_comment_view(request, slug, pk):

    template = "delete-post-comment.html"
    queryset = PostsModel.objects.get(post_slug=slug)
    comment = queryset.com_post.get(id=pk)

    if request.method == "POST":
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'You Successfully Deleted Comment')
        return redirect(queryset)

    return render(request, template, {"queryset": queryset})


@login_required(login_url="login")
def search_results_view(request):

    template = "search-results.html"

    if request.method == "POST":
        search_results = request.POST["search"]
        queryset = PostsModel.objects.filter(Q(post_title__icontains=search_results)
                                             | Q(post_user__username__icontains=search_results))

        return render(request, template, {"search_results": search_results,
                                          "queryset": queryset})
