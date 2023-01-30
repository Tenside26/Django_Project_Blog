from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUserModel, FriendModel, FriendListModel
from django.contrib import messages
from django.db.models import Q, Value
from django.db.models.functions import Concat


def user_login_view(request):
    template = "user-login.html"
    form = UserLoginForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("blog")
        else:
            messages.add_message(request, messages.INFO, 'Incorrect Password or Username')
            return redirect("login")

    return render(request, template, {"form": form})


def user_register_view(request):
    template = "user-register.html"
    form = UserRegisterForm()

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Registered Account')
            return redirect("login")

    return render(request, template, {"form": form})


@login_required(login_url="login")
def user_logout_view(request):
    template = "user-logout.html"

    if request.method == "POST":
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'You Successfully Logged Out')
        return redirect("login")

    return render(request, template, )


@login_required(login_url="login")
def user_panel_view(request, username):
    template = "user-panel.html"
    queryset = CustomUserModel.objects.get(username=username)

    return render(request, template, {"queryset": queryset})


@login_required(login_url="login")
def other_user_panel_view(request, username):
    template = "other-user-panel.html"
    queryset = CustomUserModel.objects.get(username=username)
    user_friend_list = FriendListModel.objects.get(list_owner=request.user)
    other_user_friend_list = FriendListModel.objects.get(list_owner=queryset)
    check_pending = None
    check_accepted = None
    check_send = None

    if FriendModel.objects.filter(friend_list=user_friend_list, friend=queryset, status='Pending'):
        check_pending = True

    elif FriendModel.objects.filter(friend_list=user_friend_list, friend=queryset, status='Accepted'):
        check_accepted = True

    elif FriendModel.objects.filter(friend_list=other_user_friend_list, friend=request.user, status='Pending'):
        check_send = True

    if request.method == "POST":
        FriendModel.objects.create(friend_list=user_friend_list, friend=queryset, status='Pending')
        messages.add_message(request, messages.SUCCESS,
                             'You Successfully Sent Friendship Request, Your Request Is Pending ')
        return redirect(queryset)

    return render(request, template, {"queryset": queryset,
                                      "user_friend_list": user_friend_list,
                                      "check_pending": check_pending,
                                      "check_accepted": check_accepted,
                                      "check_send": check_send})


@login_required(login_url="login")
def user_friend_list_view(request, username):

    template = "user-friend-list.html"
    queryset = CustomUserModel.objects.get(username=username)
    list_owner = queryset.list_owner
    accepted_friends_queryset = list_owner.friend_list.filter(status='Accepted')
    pending_friends_queryset = FriendModel.objects.filter(friend=queryset, status='Pending')
    send_friends_queryset = list_owner.friend_list.filter(status='Pending')

    if request.method == "POST":
        if "accept" in request.POST:
            friend_id = FriendModel.objects.get(id=request.POST["pk"])
            friend_id.status = 'Accepted'
            friend_id.save()
            FriendModel.objects.create(friend_list=list_owner, friend=friend_id.friend_list.list_owner,
                                       status='Accepted')
            messages.add_message(request, messages.INFO, 'You Accepted Friend Request')
            return redirect(list_owner)

        if "decline" in request.POST:
            friend_id = FriendModel.objects.get(id=request.POST["pk"])
            friend_id.delete()
            messages.add_message(request, messages.INFO, 'You Declined Friend Request')
            return redirect(list_owner)

        if "cancel" in request.POST:
            friend_id = FriendModel.objects.get(id=request.POST["pk"])
            friend_id.delete()
            messages.add_message(request, messages.INFO, 'You Canceled Friend Request')
            return redirect(list_owner)

        if "remove" in request.POST:
            friend_id = FriendModel.objects.get(id=request.POST["pk"])
            intertwined = FriendModel.objects.get(friend=friend_id.friend_list.list_owner, status='Accepted')
            intertwined.delete()
            friend_id.delete()
            messages.add_message(request, messages.INFO, 'You Removed Friend')
            return redirect(list_owner)

    return render(request, template, {"list_owner": list_owner,
                                      "accepted_friends_queryset": accepted_friends_queryset,
                                      "send_friends_queryset": send_friends_queryset,
                                      "pending_friends_queryset": pending_friends_queryset})


@login_required(login_url="login")
def search_friend_view(request):

    template = "search-friend.html"
    queryset = None
    friend_search = None

    if request.method == "POST":
        friend_search = request.POST["search_friend"]
        queryset = CustomUserModel.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')) \
            .filter(Q(username__icontains=friend_search)
                    | Q(first_name__icontains=friend_search)
                    | Q(last_name__icontains=friend_search)
                    | Q(full_name__icontains=friend_search)
                    | Q(age__icontains=friend_search)
                    | Q(email__icontains=friend_search))

    return render(request, template, {"friend_search": friend_search,
                                      "queryset": queryset})


@login_required(login_url="login")
def user_update_view(request, username):
    template = "user-update.html"
    queryset = CustomUserModel.objects.get(username=username)
    form = UserUpdateForm(instance=queryset)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=queryset)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Updated User Information')
            return redirect("blog")

    return render(request, template, {"form": form})


@login_required(login_url="login")
def user_password_change_view(request):
    template = "user-password-change.html"
    form = UserPasswordChangeForm(request.user)

    if request.method == "POST":
        form = UserPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You Successfully Changed Password')
            return redirect("login")

    return render(request, template, {"form": form})
