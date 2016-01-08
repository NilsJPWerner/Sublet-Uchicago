from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


from . import views


urlpatterns = [
    # url(r'^add/$', views.add, name='new_listing'),
    # # url(r'^listing/(?P<listing_id>.*)$', views.get_listing, name='Display Listing'),
    # url(r'^listing/(?P<slug>[-\w\d\_]+)/$',
    #     views.get_listing, name='display_listing'),
    # url(r'^listing/edit/(?P<slug>[-\w\d\_]+)/$',
    #     views.edit_listing, name='edit_listing'),

    url(r'^accounts/home/$', views.account_home, name='account_home'),

    url(r'^accounts/add-listing/$', views.add_listing, name='add_listing'),
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/$', views.edit_listing, name='edit_listing'),
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/description$', views.edit_listing_description, name='edit_listing_description'),
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/details$', views.edit_listing_details, name='edit_listing_details'),
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/location$', views.edit_listing_location, name='edit_listing_location'),
    
    url(r'^accounts/edit-listing/(?P<listing_id>[0-9]+)/photos$', views.edit_listing_photos, name='edit_listing_photos'),
    url(r'^upload/(?P<listing_id>[0-9]+)', views.upload, name='jfu_upload'),
    url(r'^delete/(?P<pk>\d+)$', views.upload_delete, name='jfu_delete'),

    url(r'^accounts/verification/$',
        views.account_verification, name='account_verification'),
    url(r'^accounts/disconnect/(?P<service>[0-9A-Za-z]+)',
        views.account_disconnect_service, name='account_disconnect_service'),

    url(r'^accounts/edit_profile/$', views.account_edit_profile, name='account_edit_profile'),
    
    url(r'^accounts/settings/$',
        login_required(views.account_settings.as_view()), name='account_settings'),
    url(r'^accounts/password_change_successful/$',
        TemplateView.as_view(template_name='account/password_change_successful.html'),
        name='password_change_successful'),
    url(r'^accounts/email_add_successful/$',
        login_required(views.email_add_successful.as_view()), name='email_add_successful'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 