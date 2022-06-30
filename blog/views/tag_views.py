"""Define the views for the Tag Model."""
from django.db.models.functions import Lower
from django.views.generic import DetailView, ListView

from blog.models import Tag


class TagDetailView(DetailView):
    """This will list all posts with a certain Tag slug."""

    model = Tag
    template_name = "blog/tag_detail.html"

    def get_context_data(self, **kwargs):
        """Add the page title context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Posts tagged as '{self.object.tag_name}'"

        return context


class TagListView(ListView):
    """List all the tags, and posts that are linked to them."""

    model = Tag
    template_name = "blog/tag/list.html"
    ordering = [Lower("tag_name")]

    def get_context_data(self, **kwargs):
        """Add the page title context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Tags"

        return context
