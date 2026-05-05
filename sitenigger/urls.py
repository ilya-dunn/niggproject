"""
URL configuration for sitenigger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from nigger import views  # noqa: F401
from nigger.views import page_not_found
from sitenigger import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from nigger.sitemaps import CategorySitemap, PostSitemap
from django.views.decorators.cache import cache_page


sitemaps = {
    'posts': PostSitemap,
    'cats': CategorySitemap,

}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nigger.urls')),
    path('users/', include('users.urls', namespace="users")),
    # path("__debug__/", include("debug_toolbar.urls")),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Известные негры мира'