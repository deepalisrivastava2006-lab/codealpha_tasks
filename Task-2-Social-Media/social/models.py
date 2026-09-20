from django.db import models
from django.contrib.auth.models import User


# =========================
# PROFILE
# =========================

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    bio = models.TextField(
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


# =========================
# POST
# =========================

class Post(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username + "'s Post"


# =========================
# COMMENT
# =========================

class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username + "'s Comment"


# =========================
# LIKE
# =========================

class Like(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:

        unique_together = (
            "post",
            "user"
        )


# =========================
# FOLLOW
# =========================

class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    class Meta:

        unique_together = (
            "follower",
            "following"
        )


# =========================
# NOTIFICATION
# =========================

class Notification(models.Model):

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    notification_type = models.CharField(
        max_length=20
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):

        return (
            self.sender.username
            + " -> "
            + self.recipient.username
            + " : "
            + self.notification_type
        )