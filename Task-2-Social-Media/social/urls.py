from django.urls import path
from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Register
    path(
        "register/",
        views.register,
        name="register"
    ),

    # Login
    path(
        "login/",
        views.user_login,
        name="login"
    ),

    # Logout
    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    # My Profile
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    # Other User Profile
    path(
        "user/<int:user_id>/",
        views.user_profile,
        name="user_profile"
    ),

    # Edit Profile
    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profile"
    ),

    # Like Post
    path(
        "like/<int:post_id>/",
        views.like_post,
        name="like_post"
    ),

    # Comment
    path(
        "comment/<int:post_id>/",
        views.add_comment,
        name="add_comment"
    ),

    # Follow / Unfollow
    path(
        "follow/<int:user_id>/",
        views.follow_user,
        name="follow_user"
    ),

    path(
    "notifications/",
    views.notifications,
    name="notifications"
),

path(
    "search/",
    views.search_users,
    name="search_users"
),

path(
    "delete-post/<int:post_id>/",
    views.delete_post,
    name="delete_post"
),

path(
    "edit-post/<int:post_id>/",
    views.edit_post,
    name="edit_post"
),

]