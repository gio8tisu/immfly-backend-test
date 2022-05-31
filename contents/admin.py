from django.contrib import admin

from .models import Channel, Content


class ContentInline(admin.TabularInline):
    model = Content


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Channel information",
            {"fields": ["title", "language"]},
        )
    ]
    list_display = ["id", "title"]
    inlines = [ContentInline]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Content information",
            {"fields": ["rating", "channel"]},
        )
    ]
    list_display = ["id", "rating", "channel"]
