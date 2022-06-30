"""Configure and customise the default Admin site."""
from django.contrib import admin
from django.db.models.functions import Lower
from preferences.admin import PreferencesAdmin
from secretballot.utils import get_vote_model

from blog.models import Blog, Comment, Redirect, Series, SitePreferences, Tag

Vote = get_vote_model()
admin.site.register(Vote)


class TagsInline(admin.TabularInline):
    """Define an inline class to show tags on the Blog post in Admin site."""

    model = Tag.posts.through
    extra = 1


class BlogAdmin(admin.ModelAdmin):
    """Define a custom admin class for the Blog model."""

    date_hierarchy = "created_at"
    list_display = [
        "title",
        "created_at",
        "updated_at",
        "slug",
        "user",
    ]
    list_filter = ["created_at", "updated_at"]
    ordering = ("-created_at",)
    search_fields = ["title"]
    fields = [
        "user",
        "title",
        "desc",
        "created_at",
        "updated_at",
        "body",
        "image",
        "draft",
        "slug",
        "image_attrib_name",
        "image_attrib_name_link",
        "image_attrib_site",
        "image_attrib_site_link",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "slug",
    ]
    inlines = [TagsInline]


class CommentAdmin(admin.ModelAdmin):
    """Define a custom admin class for the Comment model."""

    list_display = ["__str__", "id", "created_at", "updated_at"]


class TagsAdmin(admin.ModelAdmin):
    """Define a custom admin class for the Tag Model."""

    list_display = ["tag_name", "pk", "tag_count", "tag_creator"]
    ordering = (Lower("tag_name"),)
    readonly_fields = ["slug"]


class SeriesAdmin(admin.ModelAdmin):
    """Define a custom admin class for the Series model."""

    list_display = ["series_name", "pk", "series_creator"]
    ordering = (Lower("series_name"),)
    readonly_fields = ["slug"]


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Redirect)
admin.site.register(Series, SeriesAdmin)
admin.site.register(SitePreferences, PreferencesAdmin)
