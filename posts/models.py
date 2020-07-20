from markdown import markdown as md

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.timezone import now


class Tag(models.Model):
    name: models.CharField = models.CharField(max_length=200, unique=True)
    slug: models.SlugField = models.SlugField(max_length=200, unique=True)
    color_code: models.CharField = models.CharField(max_length=7)

    class Meta:
        ordering = ("name",)

    def colored_code(self):
        return format_html('<span style="color: {0};"> {0}</span>', self.color_code)

    def get_absolute_url(self):
        return reverse("posts:tag_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DraftsPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_draft=True)


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_draft=False)


class Post(models.Model):

    title: models.CharField = models.CharField(max_length=200, unique=True)
    slug: models.SlugField = models.SlugField(max_length=200, unique=True)
    pub_date: models.DateTimeField = models.DateTimeField(default=now)
    tags: models.ManyToManyField = models.ManyToManyField(
        Tag, blank=True, related_name="posts"
    )
    content: models.TextField = models.TextField()
    markdown: models.TextField = models.TextField(blank=True)
    author: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    is_draft: models.BooleanField = models.BooleanField(default=True)

    objects: models.Manager = models.Manager()  # The default manager.
    published = PublishedPostManager()
    drafts = DraftsPostManager()

    class Meta:
        ordering = ("-pub_date",)

    def get_absolute_url(self):
        return reverse("posts:post_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        self.markdown = md(
            self.content,
            extensions=["fenced_code", "codehilite"],
        )
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
