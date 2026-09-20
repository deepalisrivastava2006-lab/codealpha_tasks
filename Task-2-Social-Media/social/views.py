from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import (
    Profile,
    Post,
    Like,
    Comment,
    Follow,
    Notification
)


# =========================
# HOME
# =========================

@login_required
def home(request):

    # =========================
    # CREATE POST
    # =========================

    if request.method == "POST":

        content = request.POST.get(
            "content",
            ""
        ).strip()

        image = request.FILES.get(
            "image"
        )

        if content or image:

            Post.objects.create(
                user=request.user,
                content=content,
                image=image
            )

            messages.success(
                request,
                "Post created successfully!"
            )

            return redirect("home")


    # =========================
    # ALL POSTS
    # =========================

    posts = Post.objects.all().order_by(
        "-created_at"
    )


    # =========================
    # PEOPLE TO FOLLOW
    # =========================

    users = User.objects.exclude(
        id=request.user.id
    )

    following_ids = set(
        Follow.objects.filter(
            follower=request.user
        ).values_list(
            "following_id",
            flat=True
        )
    )

    users_with_follow_status = [
        (
            user,
            user.id in following_ids
        )
        for user in users
    ]


    # =========================
    # LIKED POSTS
    # =========================

    liked_post_ids = set(
        Like.objects.filter(
            user=request.user
        ).values_list(
            "post_id",
            flat=True
        )
    )


    # =========================
    # UNREAD NOTIFICATIONS
    # =========================

    unread_notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()


    # =========================
    # SEND DATA TO TEMPLATE
    # =========================

    return render(
        request,
        "social/home.html",
        {
            "posts": posts,

            "users": users,

            "users_with_follow_status":
                users_with_follow_status,

            "liked_post_ids":
                liked_post_ids,

            "unread_notifications":
                unread_notifications,
        }
    )


# =========================
# REGISTER
# =========================

def register(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        email = request.POST.get(
            "email"
        )

        password = request.POST.get(
            "password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )


        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect(
                "register"
            )


        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect(
                "register"
            )


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        Profile.objects.create(
            user=user
        )


        messages.success(
            request,
            "Account created successfully!"
        )

        return redirect(
            "login"
        )


    return render(
        request,
        "social/register.html"
    )


# =========================
# LOGIN
# =========================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                "home"
            )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )


    return render(
        request,
        "social/login.html"
    )


# =========================
# LOGOUT
# =========================

def user_logout(request):

    logout(request)

    return redirect(
        "login"
    )


# =========================
# MY PROFILE
# =========================

@login_required
def profile(request):

    user_profile, created = Profile.objects.get_or_create(
        user=request.user
    )


    followers_count = Follow.objects.filter(
        following=request.user
    ).count()


    following_count = Follow.objects.filter(
        follower=request.user
    ).count()


    user_posts = Post.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )


    liked_post_ids = set(
        Like.objects.filter(
            user=request.user
        ).values_list(
            "post_id",
            flat=True
        )
    )


    posts_with_like_status = [
        (
            post,
            post.id in liked_post_ids
        )
        for post in user_posts
    ]


    return render(
        request,
        "social/profile.html",
        {
            "profile": user_profile,

            "followers_count":
                followers_count,

            "following_count":
                following_count,

            "posts_with_like_status":
                posts_with_like_status
        }
    )


# =========================
# OTHER USER PROFILE
# =========================

@login_required
def user_profile(request, user_id):

    user = User.objects.get(
        id=user_id
    )


    user_profile, created = Profile.objects.get_or_create(
        user=user
    )


    is_following = Follow.objects.filter(
        follower=request.user,
        following=user
    ).exists()


    followers_count = Follow.objects.filter(
        following=user
    ).count()


    following_count = Follow.objects.filter(
        follower=user
    ).count()


    user_posts = Post.objects.filter(
        user=user
    ).order_by(
        "-created_at"
    )


    liked_post_ids = set(
        Like.objects.filter(
            user=request.user
        ).values_list(
            "post_id",
            flat=True
        )
    )


    posts_with_like_status = [
        (
            post,
            post.id in liked_post_ids
        )
        for post in user_posts
    ]


    return render(
        request,
        "social/user_profile.html",
        {
            "profile": user_profile,

            "is_following":
                is_following,

            "followers_count":
                followers_count,

            "following_count":
                following_count,

            "posts_with_like_status":
                posts_with_like_status
        }
    )


# =========================
# EDIT PROFILE
# =========================

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )


    if request.method == "POST":

        bio = request.POST.get(
            "bio"
        )

        profile.bio = bio


        if request.FILES.get(
            "profile_picture"
        ):

            profile.profile_picture = request.FILES.get(
                "profile_picture"
            )


        profile.save()


        messages.success(
            request,
            "Profile updated successfully!"
        )


        return redirect(
            "profile"
        )


    return render(
        request,
        "social/edit_profile.html",
        {
            "profile": profile
        }
    )


# =========================
# LIKE / UNLIKE POST
# =========================

@login_required
def like_post(request, post_id):

    post = Post.objects.get(
        id=post_id
    )


    like = Like.objects.filter(
        post=post,
        user=request.user
    ).first()


    if like:

        like.delete()

        liked = False

    else:

        Like.objects.create(
            post=post,
            user=request.user
        )

        liked = True


        if post.user != request.user:

            Notification.objects.create(
                recipient=post.user,
                sender=request.user,
                notification_type="like",
                post=post
            )


    likes_count = Like.objects.filter(
        post=post
    ).count()


    return JsonResponse(
        {
            "liked": liked,
            "likes_count": likes_count
        }
    )


# =========================
# ADD COMMENT
# =========================

@login_required
def add_comment(request, post_id):

    post = Post.objects.get(
        id=post_id
    )


    if request.method == "POST":

        text = request.POST.get(
            "text",
            ""
        ).strip()


        if text:

            comment = Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )


            return JsonResponse(
                {
                    "success": True,

                    "username":
                        request.user.username,

                    "text":
                        comment.text,

                    "created_at":
                        comment.created_at.strftime(
                            "%d %b %Y, %I:%M %p"
                        )
                }
            )


    return JsonResponse(
        {
            "success": False
        }
    )


# =========================
# FOLLOW / UNFOLLOW
# =========================

@login_required
def follow_user(request, user_id):

    user_to_follow = User.objects.get(
        id=user_id
    )


    if user_to_follow == request.user:

        return JsonResponse(
            {
                "error":
                    "You cannot follow yourself."
            }
        )


    follow = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    ).first()


    if follow:

        # UNFOLLOW

        follow.delete()


        Notification.objects.filter(
            recipient=user_to_follow,
            sender=request.user,
            notification_type="follow"
        ).delete()


        is_following = False


    else:

        # FOLLOW

        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )


        Notification.objects.create(
            recipient=user_to_follow,
            sender=request.user,
            notification_type="follow"
        )


        is_following = True


    followers_count = Follow.objects.filter(
        following=user_to_follow
    ).count()


    return JsonResponse(
        {
            "is_following":
                is_following,

            "followers_count":
                followers_count
        }
    )


# =========================
# NOTIFICATIONS
# =========================

@login_required
def notifications(request):

    user_notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by(
        "-created_at"
    )


    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(
        is_read=True
    )


    return render(
        request,
        "social/notifications.html",
        {
            "notifications":
                user_notifications
        }
    )


# =========================
# SEARCH USERS
# =========================

@login_required
def search_users(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()


    users = User.objects.none()


    if query:

        users = User.objects.filter(
            username__icontains=query
        ).exclude(
            id=request.user.id
        )


    return render(
        request,
        "social/search_users.html",
        {
            "users": users,

            "query": query
        }
    )


# =========================
# DELETE POST
# =========================

@login_required
def delete_post(request, post_id):

    post = Post.objects.get(
        id=post_id
    )


    if post.user != request.user:

        return redirect(
            "home"
        )


    if request.method == "POST":

        post.delete()


    return redirect(
        "home"
    )


# =========================
# EDIT POST
# =========================

@login_required
def edit_post(request, post_id):

    post = Post.objects.get(
        id=post_id
    )


    if post.user != request.user:

        return redirect(
            "home"
        )


    if request.method == "POST":

        content = request.POST.get(
            "content",
            ""
        ).strip()


        image = request.FILES.get(
            "image"
        )


        if content:

            post.content = content


        if image:

            post.image = image


        post.save()


        messages.success(
            request,
            "Post updated successfully!"
        )


        return redirect(
            "home"
        )


    return render(
        request,
        "social/edit_post.html",
        {
            "post": post
        }
    )