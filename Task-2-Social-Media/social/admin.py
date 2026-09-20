from django.contrib import admin
from .models import Profile, Post, Comment, Like, Follow, Notification


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "sender",
        "notification_type",
        "created_at",
        "is_read",
    )

    list_filter = (
        "notification_type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "recipient__username",
        "sender__username",
    )