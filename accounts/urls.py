from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
	# url(r'^$', views.home, name='home'),
	url(r'^add/$', views.add, name='New Listing'),
	url(r'^listing/(?P<listing_id>.*)$', views.get_listing, name='Display Listing')
]