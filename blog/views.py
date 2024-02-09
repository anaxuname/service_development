from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from blog.models import Blog


class ContentManagerRequiredMixin(AccessMixin):
    """Verify that the current user is content manager."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_content_manager():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class BlogCreateView(ContentManagerRequiredMixin, CreateView):
    model = Blog
    permission_required = "main.add_blog"
    fields = ("title", "body", "is_public")
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(ContentManagerRequiredMixin, UpdateView):
    model = Blog
    fields = ("title", "body", "is_public")
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:view", args=[self.kwargs.get("pk")])


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_public=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class BlogDeleteView(ContentManagerRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:list")
