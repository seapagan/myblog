"""Define URL patterns for the Blog app."""
from django.urls import path

from blog.views import blog_views, comment_views, series_views, tag_views

app_name = "blog"
urlpatterns = [
    # Blog Views
    path(
        "",
        blog_views.IndexClassView.as_view(),
        name="index",
    ),
    path(
        "<str:slug>",
        blog_views.PostDetailView.as_view(),
        name="detail",
    ),
    path(
        "new/",
        blog_views.NewPostView.as_view(),
        name="add_post",
    ),
    path(
        "<str:slug>/edit",
        blog_views.EditPostView.as_view(),
        name="edit_post",
    ),
    path(
        "<str:slug>/delete",
        blog_views.DeletePostView.as_view(),
        name="delete_post",
    ),
    # search
    path("search/", blog_views.SearchView.as_view(), name="search"),
    # Comment Views
    path(
        "<str:slug>/comment",
        comment_views.AddCommentView.as_view(),
        name="add_comment",
    ),
    path(
        "comment/<int:pk>/edit",
        comment_views.EditCommentView.as_view(),
        name="edit_comment",
    ),
    path(
        "comment/<int:pk>/delete",
        comment_views.DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    # Tag Views
    path(
        "tags/<str:slug>/",
        tag_views.TagDetailView.as_view(),
        name="tag_detail",
    ),
    path(
        "tags/",
        tag_views.TagListView.as_view(),
        name="tag_list",
    ),
    # Series Views
    path(
        "series/<str:slug>",
        series_views.SeriesDetailView.as_view(),
        name="series_detail",
    ),
    path(
        "series/",
        series_views.SeriesListView.as_view(),
        name="series_list",
    ),
]
