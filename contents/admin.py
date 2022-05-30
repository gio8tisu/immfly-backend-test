from django.contrib import admin

from .models import Channel


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Channel information",
            {"fields": ["title", "language"]},
        )
    ]
    list_display = ["id", "title"]
