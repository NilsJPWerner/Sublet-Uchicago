from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^accounts/add-listing/$', views.add_listing, name='add_listing'),
    url(r'^accounts/publish/(?P<listing_id>[0-9]+)/$', views.publish_listing, name='publish_listing'),
    url(r'^accounts/unpublish/(?P<listing_id>[0-9]+)/$', views.unpublish_listing, name='unpublish_listing'),
    url(r'^accounts/delete/(?P<listing_id>[0-9]+)/$', views.delete_listing, name='delete_listing'),

    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/$', views.edit_listing, name='edit_listing'),
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/description$', views.edit_listing_description, name='edit_listing_description'),
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/details$', views.edit_listing_details, name='edit_listing_details'),
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/location$', views.edit_listing_location, name='edit_listing_location'),
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/photos$', views.edit_listing_photos, name='edit_listing_photos'),
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/calendar$', views.edit_listing_calendar, name='edit_listing_calendar'),

    # Ajax photo upload views
    url(r'^upload/(?P<listing_id>[0-9]+)', views.upload, name='jfu_upload'),
    url(r'^delete/(?P<pk>\d+)$', views.upload_delete, name='jfu_delete'),
]
