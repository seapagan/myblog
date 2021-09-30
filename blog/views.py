"""Define the views for the 'blog' application."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.urls.base import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView

from blog.forms import EditCommentForm, EditPostForm, NewCommentForm
from blog.models import Blog, Comment


class IndexClassView(ListView):
    """Define a TemplateView for the index (Blog main page)."""

    template_name = "blog/index.html"
    context_object_name = "blogs"
    paginate_by = 6
    model = Blog


# class IndexClassView(TemplateView):
#     """Define a TemplateView for the index (Blog main page)."""

#     template_name = "blog/index.html"
#     paginate_by = 6

#     def get_context_data(self, **kwargs):
#         """Return the context for this view.

#         Doing it this way (and not using a ListView so as to enable multiple
#         models to be shown in the template (eg comment counts etc).
#         """
#         context = super(IndexClassView, self).get_context_data(**kwargs)
#         context["blogs"] = Blog.objects.all().order_by("-created_at")

#         return context


class PostDetailView(DetailView):
    """Display an actual blog post."""

    model = Blog
    template = "blog/detail.html"


class NewPostView(LoginRequiredMixin, CreateView):
    """Add a new post to the Blog."""

    model = Blog
    fields = ["title", "desc", "body"]
    template_name = "blog/blog_newpost.html"

    def form_valid(self, form):
        """Validate the form."""
        form.instance.user = self.request.user

        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, UpdateView):
    """Edit an existing Post."""

    model = Blog
    form_class = EditPostForm
    template_name = "blog/blog_editpost.html"

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        post_slug = Blog.objects.get(slug=self.kwargs["slug"]).slug
        print(post_slug)
        return reverse("blog:detail", kwargs={"slug": post_slug})

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the post.

        Also can edit if they are a superuser.
        """
        obj = super(EditPostView, self).get_object()
        if (
            not obj.user == self.request.user
            and not self.request.user.is_superuser
        ):
            raise Http404("You Dont have permission to do that!")
        return obj


class DeletePostView(LoginRequiredMixin, DeleteView):
    """Edit an existing Post."""

    model = Blog
    # template_name = "blog/blog_deletepost.html"

    success_url = reverse_lazy("blog:index")

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the post.

        Also can delete if they are a superuser.
        """
        obj = super(DeletePostView, self).get_object()
        if (
            not obj.user == self.request.user
            and not self.request.user.is_superuser
        ):
            raise Http404("You Dont have permission to do that!")
        return obj


class AddCommentView(CreateView):
    """Add a new comment to a specific post."""

    model = Comment
    form_class = NewCommentForm
    template_name = "blog/comment_newcomment.html"

    def get_context_data(self, **kwargs):
        """Add extra context to the View.

        This allows us to access Post-related stuff like the title from inside
        our view.
        """
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        context["post"] = Blog.objects.get(slug=slug)
        context["form"].related_post = context["post"]
        return context

    def form_valid(self, form):
        """Validate the form."""
        form.instance.related_post_id = Blog.objects.get(
            slug=self.kwargs["slug"]
        ).id
        if self.request.user:
            form.instance.created_by_user_id = self.request.user.id
        # else:
        #     form.instance.created_by_guest = "Guest User"

        return super().form_valid(form)

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        return reverse("blog:detail", kwargs={"slug": self.kwargs["slug"]})


class EditCommentView(LoginRequiredMixin, UpdateView):
    """Edit an existing comment ."""

    model = Comment
    form_class = EditCommentForm
    template_name = "blog/comment_editcomment.html"

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        post_slug = Comment.objects.get(pk=self.kwargs["pk"]).related_post.slug
        return reverse("blog:detail", kwargs={"slug": post_slug})

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the comment."""
        obj = super(EditCommentView, self).get_object()
        if (
            not obj.created_by_user == self.request.user
            and not self.request.user.is_superuser
        ):
            raise Http404("You Dont have permission to do that!")
        return obj


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    """Delete an existing comment."""

    model = Comment

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        post_slug = Comment.objects.get(pk=self.kwargs["pk"]).related_post.slug
        return reverse("blog:detail", kwargs={"slug": post_slug})

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the comment."""
        obj = super(DeleteCommentView, self).get_object()
        if (
            not obj.created_by_user == self.request.user
            and not self.request.user.is_superuser
        ):
            raise Http404("You Dont have permission to do that!")
        return obj
