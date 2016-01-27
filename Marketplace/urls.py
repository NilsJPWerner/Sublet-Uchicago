from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('accounts.urls', namespace="accounts")),
    url(r'^', include('listings.urls', namespace="listings")),

    # Static pages
    url(r'^$', TemplateView.as_view(template_name="Marketplace/home.html"), name="home"),
    url(r'^map/', TemplateView.as_view(template_name="Marketplace/map.html"), name="map"),

    # Ajax search
    url(r'^search/$', views.ajax_listing_search, name="search"),

    # Profile tools
    url(r'^accounts/', include('allauth.urls'), name='accounts'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
