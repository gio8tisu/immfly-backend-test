from django.contrib import admin

from .models import Author, Channel, ChannelLanguage, Content, ContentGenre


class ContentInline(admin.TabularInline):
    model = Content


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Channel information",
            {"fields": ["title", "language", "picture"]},
        )
    ]
    list_display = ["id", "title"]
    inlines = [ContentInline]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Content information",
            {
                "fields": [
                    "file",
                    "rating",
                    "channel",
                    "genre",
                    "description",
                    "authors",
                ]
            },
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


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Author information",
            {"fields": ["name", "surname"]},
        )
    ]
    list_display = ["id", "full_name"]


@admin.register(ContentGenre)
class ContentGenreAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Genre information",
            {"fields": ["name"]},
        )
    ]
    list_display = ["id", "name"]
