"""Define the views for the Series Model."""
from django.db.models.functions import Lower
from django.views.generic import DetailView, ListView

from blog.models import Series


class SeriesDetailView(DetailView):
    """This will list all posts in the Series with the slug."""

    model = Series
    template_name = "blog/series_detail.html"

    def get_context_data(self, **kwargs):
        """Add the Page Title context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Series | '{self.object.series_name}'"

        return context


class SeriesListView(ListView):
    """List all the Series, and posts that are linked to them."""

    model = Series
    template_name = "blog/series/list.html"
    ordering = [Lower("series_name")]

    def get_context_data(self, **kwargs):
        """Add the Page Title context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Series"

        return context
