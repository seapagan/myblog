"""Define the Database models for this application."""
import os

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from hitcount.conf import settings as hitcount_settings
from hitcount.mixins import HitCountModelMixin
from preferences.models import Preferences


class OverwriteStorage(FileSystemStorage):
    """Returns a filename that's free on the target storage system.

    Will delete any file with the same name.
    """

    def get_available_name(self, name, max_length=None):
        """Override the get_available_name, to delete existing file."""
        self.delete(name)
        super().get_available_name(name, max_length)
        return name


def get_upload_path(instance, filename):
    """Helper function to get a user-specific upload path.

    We rename the file to "header_image" with the existing extension. This
    should stop the media dirs being cluttered if the image changes.
    """
    ext = os.path.splitext(filename)[1]
    filename = "header_image" + ext
    return os.path.join("posts", instance.slug, filename)


class Blog(models.Model, HitCountModelMixin):
    """Define the blog model.

    This will contain individual blog entries.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name="blog_posts"
    )
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = RichTextUploadingField(config_name="post")
    slug = models.SlugField(default="", unique=True)
    image = models.ImageField(
        upload_to=get_upload_path,
        null=True,
        storage=OverwriteStorage(),
        blank=True,
    )
    draft = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(
        hitcount_settings.HITCOUNT_HITCOUNT_MODEL,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )
    image_attrib_name = models.CharField(
        max_length=50,
        default="",
        blank=True,
    )
    image_attrib_name_link = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    image_attrib_site = models.CharField(
        max_length=50,
        default="",
        blank=True,
    )
    image_attrib_site_link = models.URLField(
        max_length=200,
        default="",
        blank=True,
    )

    class Meta:
        """Meta configuration for the Blog model."""

        ordering = ["-created_at"]

    def __str__(self):
        """Return string representation of the Blog object."""
        return self.title

    def save(self, *args, **kwargs):
        """Override the save function, so we can generate the slug."""
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Override get_absolute_url function."""
        return reverse("blog:detail", args=[self.slug])

    def no_of_comments(self):
        """Count comments on this post."""
        return Comment.objects.filter(related_post=self).count()

    def has_image_meta(self):
        """Return true if this post has any image metadata."""
        return (
            self.image_attrib_name != ""
            or self.image_attrib_name_link != ""
            or self.image_attrib_site != ""
            or self.image_attrib_site_link != ""
        )


class Comment(models.Model):
    """Define the 'Comment' Model."""

    created_by_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="comments",
    )
    created_by_guest = models.CharField(max_length=50, blank=True)
    guest_email = models.EmailField(blank=True)
    related_post = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = RichTextField(config_name="comment", blank=True)

    class Meta:
        """Meta configuration for the Blog model."""

        ordering = ["created_at"]

    def __str__(self):
        """Return string representation of the Comment object."""
        return (
            f"Comment by '{self.get_commenter()}' "
            f"on post: '{self.related_post}'"
        )

    def get_commenter(self):
        """Return either the logged in user name or temp user name."""
        return (
            self.created_by_user.username
            if self.created_by_user
            else self.created_by_guest
        )


class SitePreferences(Preferences):
    """Define the global site settings."""

    sitename = models.CharField(max_length=50, default="My Sexy Blog")
    title = models.CharField(max_length=20, default="My Blog")
    heading = models.CharField(
        max_length=200, default="A blog of blogging blogosity."
    )
    pinned_post = models.ForeignKey(
        Blog, null=True, blank=True, on_delete=models.CASCADE
    )
    twitter_site = models.CharField(max_length=50, default="")

    class Meta:
        """class-specific configuration."""

        verbose_name_plural = "Site Preferences"


def post_count(self):
    """Helper function to get the count of posts with this tag."""
    return self.posts.all().count()


class Tag(models.Model):
    """Define the Tags model."""

    tag_name = models.CharField(max_length=15)
    tag_count = post_count
    tag_creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tags"
    )
    slug = models.SlugField(default="", unique=True)
    posts = models.ManyToManyField(Blog, blank=True)

    def __str__(self):
        """Define the Text version of this object."""
        return f"{self.tag_name}"

    def save(self, *args, **kwargs):
        """Override the save function, so we can generate the slug."""
        self.slug = slugify(self.tag_name)
        super().save(*args, **kwargs)


class Redirect(models.Model):
    """Define the Redirect model."""

    old_slug = models.SlugField(default="", unique=True)
    old_post = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        """Define the Text version of this object."""
        return f"{self.old_slug} -> {self.old_post}"


class Series(models.Model):
    """Define the Series model."""

    series_name = models.CharField(max_length=50)
    series_creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="series"
    )
    description = RichTextField(config_name="comment", blank=True)
    slug = models.SlugField(default="", unique=True)
    posts = models.ManyToManyField(Blog, blank=True)

    class Meta:
        """Set up Class Metadata."""

        verbose_name_plural = "Series"

    def __str__(self):
        """Define the Text version of this object."""
        return f"{self.series_name}"

    def save(self, *args, **kwargs):
        """Override the save function, so we can generate the slug."""
        self.slug = slugify(self.series_name)
        super().save(*args, **kwargs)
