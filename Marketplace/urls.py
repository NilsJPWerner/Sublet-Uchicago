from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('accounts.urls', namespace="accounts")),
    
    # Static pages
    url(r'^$', TemplateView.as_view(template_name="Marketplace/home.html")),
    url(r'^map/$', TemplateView.as_view(template_name="Marketplace/map.html")),

    # Profile tools
    url(r'^accounts/', include('allauth.urls'), name='accounts'),
]
