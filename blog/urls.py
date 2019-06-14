from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from posts.views import index
from posts.sitemap import BlogSitemap

urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("posts/", include("posts.urls", namespace="posts")),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"blog": BlogSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
