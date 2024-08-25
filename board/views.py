from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .filters import PostFilter

from .models import (
    Post,
    Comment,
)

from .forms import (
    PostForm,
    CommentForm,
    AcceptCommentForm,
)


# Create your views here.


class PostsList(ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"


class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk)
        comments = post.comment_set.all()

        context["post"] = post
        context["comments"] = comments
        context["form"] = form
        return context


class PostEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"


class ReviewsList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = "user_posts_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        queryset = Comment.objects.filter(post__author=self.request.user)
        self.filterset = PostFilter(
            self.request.GET, queryset, request=self.request.user
        )
        if self.request.GET:
            return self.filterset.qs
        return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("posts")


class ReviewDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    success_url = reverse_lazy("reviews_list")


class AcceptReview(LoginRequiredMixin, UpdateView):
    form_class = AcceptCommentForm
    model = Comment
    template_name = "accept_comment.html"


@login_required
def create_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return HttpResponseRedirect("/")
    return render(request, "post_create.html", {"form": form})


@login_required
def create_comment_to_post(request, pk):
    form = CommentForm()
    post = Post.objects.get(pk=int(pk))
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return HttpResponseRedirect(f"/{pk}")
    return render(request, "comment_create.html", {"form": form, "post": post})
