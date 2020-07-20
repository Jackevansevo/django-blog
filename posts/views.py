from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe
from django.views.generic.dates import MonthArchiveView
from django.views.generic.detail import DetailView

from .models import Post, Tag

# [TODO]
# - 100% Test coverage
# - Docker
# - Abstract out unique blog functionality
# - Config file
#   - About
#   - Blog title
#   - Social media links etc.
# - Static files (i.e. uploadable images to put in blog posts)


def index(request):

    tags = Tag.objects.all()

    if request.user.is_anonymous:
        # Only show published posts
        posts = Post.published.all()
        tags = tags.annotate(count=Count("posts", filter=Q(posts__is_draft=False)))
    else:
        posts = Post.objects.all()
        tags = tags.annotate(count=Count("posts"))

    posts = posts.select_related("author").prefetch_related("tags")

    # Count the number of posts per tag
    tags = tags.filter(count__gte=1).order_by("-count")

    # Only show publised posts in the archive
    archived_months = posts.filter(is_draft=False).dates(
        "pub_date", "month", order="DESC"
    )

    # Paginate the posts
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(
        request,
        "posts/index.html",
        {"posts": posts, "archive": archived_months, "tags": tags},
    )


@login_required
def post_publish(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author != request.user:
        raise PermissionDenied

    post.is_draft = False
    post.save(update_fields=["is_draft"])
    return redirect(post)


def post_search(request):
    query = request.GET.get("q")
    posts = Post.published.filter(title__contains=query)
    return render(request, "posts/post_search.html", {"posts": posts})


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.posts.all()
    if request.user.is_anonymous:
        posts = posts.exclude(is_draft=True)
    return render(request, "posts/tag_detail.html", {"tag": tag, "posts": posts})


class PostDetail(DetailView):

    model = Post
    template = "posts/post_detail.html"

    def get_object(self, queryset=None):
        obj = super(PostDetail, self).get_object(queryset=queryset)
        if obj.is_draft and self.request.user.is_anonymous:
            raise Http404()

        return obj


class PostMonthArchiveView(MonthArchiveView):

    queryset = Post.published.all()
    date_field = "pub_date"
    context_object_name = "posts"


class LatestPostsFeed(Feed):

    title = "Jacks Blog"
    link = "/posts/"
    description = "Recent content on Jacks Blog"

    def items(self):
        return Post.published.all()

    def item_pubdate(self, item):
        return item.pub_date

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return mark_safe(item.markdown)
