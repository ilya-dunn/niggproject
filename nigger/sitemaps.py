from django.contrib.sitemaps import Sitemap
from .models import Category, Nigger

class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Nigger.published.all()

    def lastmod(self, obj):
        return obj.time_update


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Category.objects.all()