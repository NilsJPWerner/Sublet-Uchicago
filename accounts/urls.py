from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    # url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add, name='new_listing'),
    # url(r'^listing/(?P<listing_id>.*)$', views.get_listing, name='Display Listing'),
    url(r'^listing/(?P<slug>[-\w\d\_]+)/$', views.get_listing, name='display_listing'),
    url(r'^listing/edit/(?P<slug>[-\w\d\_]+)/$', views.edit_listing, name='edit_listing'),
    
    url(r'^accounts/home/$', views.account_home, name='account_home'),
    url(r'^accounts/verification/$', views.account_verification, name='account_verification'),
    url(r'^accounts/disconnect/(?P<service>[0-9A-Za-z]+)', views.account_disconnect_service, name='account_disconnect_service'),
    url(r'^accounts/edit_profile/$', views.account_edit_profile, name='account_edit_profile'),
    url(r'^accounts/settings/$', login_required(views.account_settings.as_view()), name='account_settings'),
    url(r'^accounts/password_change_successful/$',
        TemplateView.as_view(template_name='account/password_change_successful.html'),
        name='password_change_successful'),
    url(r'^accounts/email_add_successful/$', login_required(views.email_add_successful.as_view()), name='email_add_successful'),
]
