from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    # url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add, name='new_listing'),
    # url(r'^listing/(?P<listing_id>.*)$', views.get_listing, name='Display Listing'),
    url(r'^listing/(?P<slug>[-\w\d\_]+)/$', views.get_listing, name='display_listing'),
    url(r'^listing/edit/(?P<slug>[-\w\d\_]+)/$', views.edit_listing, name='edit_listing'),
    url(r'^accounts/home/$', views.account_home, name='account_home'),
]