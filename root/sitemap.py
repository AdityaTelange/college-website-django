from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class ViewSitemap(Sitemap):
    def items(self):
        return ['about_us', 'contact_us']

    def location(self, obj):
        return reverse(obj)
