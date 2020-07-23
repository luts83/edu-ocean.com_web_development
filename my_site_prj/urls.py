"""my_site_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
    path('studyroom/', include('studyroom.urls')),
    path('', include('basecamp.urls')),
    path('robots.txt/', lambda x: HttpResponse("User-Agent:*\nDisallow: ",
                                               content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': {'post': GenericSitemap(sitemap_dict, priority=0.6, protocol='http')}},
         name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

sitemap_dict = {
    'queryset': Post.objects.filter(is_active=True).order_by('-updated_at'),
    'date_field': 'updated_at',
}