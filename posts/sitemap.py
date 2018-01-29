from django.contrib.sitemaps import Sitemap
from posts.models import Post


class BlogSitemap(Sitemap):
    priority = 0.5
    changefreq = "never"

    def items(self):
        return Post.objects.filter(is_draft=False)

    def lastmod(self, obj):
        return obj.pub_date
