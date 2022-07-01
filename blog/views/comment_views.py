"""Define the views for the Comment Model."""
import smtplib

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http.response import Http404
from django.urls.base import reverse
from django.utils.html import strip_tags
from django.views.generic import CreateView
from django.views.generic.edit import DeleteView, UpdateView

from blog.forms import EditCommentForm, NewCommentForm
from blog.models import Blog, Comment


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
        context["page_title"] = "New Comment"

        return context

    def get_form_kwargs(self):
        """Add the User to the form kwargs."""
        kwargs = super(AddCommentView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Validate the form."""
        related_post = Blog.objects.get(slug=self.kwargs["slug"])
        form.instance.related_post_id = related_post.id
        if self.request.user.is_authenticated:
            form.instance.created_by_user_id = self.request.user.id

        # send an email to the post author
        html_message = (
            "A new comment has been added to your post:"
            f" '<b>{related_post.title}</b>'\n\n"
        )
        html_message += f"{form.instance.body}\n"
        message = strip_tags(html_message)
        try:
            send_mail(
                subject=f"New comment on {related_post.title}",
                message=message,
                html_message=html_message,
                from_email="noreply@tekcited.net",
                recipient_list=[related_post.user.email],
            )
        except smtplib.SMTPException as e:
            print(f"Cant send email: {e}")

        return super().form_valid(form)

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        return reverse("blog:detail", kwargs={"slug": self.kwargs["slug"]})


class EditCommentView(LoginRequiredMixin, UpdateView):
    """Edit an existing comment ."""

    model = Comment
    form_class = EditCommentForm
    template_name = "blog/comment_editcomment.html"

    def get_context_data(self, **kwargs):
        """Add extra context to the View."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Comment"

        return context

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

    def get_context_data(self, **kwargs):
        """Add extra context to the View."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Comment"

        return context

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
