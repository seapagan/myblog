"""Several custom Template tags to make things easier."""
from django import template
from django.db.models import Q
from django.db.models.functions import Lower

from blog.models import Blog, Series, Tag

register = template.Library()


@register.filter()
def no_draft(tag_posts, user=None):
    """Filter draft posts out of the queryset."""
    # try to use the user (so we can see our own draft posts in the tag list),
    # if we get an exception then we are not logged in so it doesn't matter and
    # we just hide all draft posts
    try:
        filtered = tag_posts.exclude(Q(draft=True) & ~Q(user=user))
    except TypeError:
        filtered = tag_posts.exclude(draft=True)
    return filtered


@register.filter()
def by_hits(posts):
    """Sort the posts Queryset by hits."""
    return posts.order_by(
        "-hit_count_generic__hits", "-total_upvotes", "-created_at"
    )


# the below tag is used in the sidebar to pass extra context that is needed to
# get the sidebar to work.
@register.simple_tag
def sidebar():
    """Provide extra information needed for the sidebar."""
    context = {}

    # Return first 5 posts in the database.
    context["posts"] = (
        Blog.objects.all().exclude(draft=True).order_by("-created_at")[:6]
    )

    # return all Article Series.
    context["series"] = Series.objects.all().order_by("-id")[:6]

    # Return all Tags.
    # will later most likely restrict tags to the top 20 or so tags sorted by
    # number of related posts, for now send all.
    context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))

    # set a filtered context for popular posts, sorted by views then likes.
    popular_posts = (
        Blog.objects.all()
        .exclude(
            Q(draft=True)
            | Q(hit_count_generic__hits=0)
            | Q(hit_count_generic__hits=None)
        )
        .order_by("-hit_count_generic__hits", "-total_upvotes", "-created_at")[
            :6
        ]
    )
    context["popular"] = popular_posts

    #  empty each context (for troubleshooting)
    # context["posts"] = ()
    # context["tags"] = ()
    # context["popular"] = ()
    return context
