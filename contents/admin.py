from django.contrib import admin

from .models import Channel, ChannelLanguage, Content


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


@admin.register(ChannelLanguage)
class ChannelLanguageAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Language information",
            {"fields": ["code", "language"]},
        )
    ]
    list_display = ["id", "code", "language"]
