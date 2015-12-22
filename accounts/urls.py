from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    # url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add, name='new_listing'),
    # url(r'^listing/(?P<listing_id>.*)$', views.get_listing, name='Display Listing'),
    url(r'^listing/(?P<slug>[-\w\d\_]+)/$', views.get_listing, name='display_listing'),
    url(r'^listing/edit/(?P<slug>[-\w\d\_]+)/$', views.edit_listing, name='edit_listing'),
    url(r'^accounts/home/$', views.account_home, name='account_home'),
    url(r'^accounts/verification/$', views.account_verification, name='account_verification'),
    url(r'^accounts/edit_profile/$', views.account_edit_profile, name='account_edit_profile'),
    url(r'^accounts/settings/$', views.account_settings, name='account_settings'),
    url(r'^accounts/password_change_successful/$', 
      TemplateView.as_view(template_name='account/password_change_successful.html'),
      name='password_change_successful'),
    url(r'^accounts/test/$', views.test.as_view(), name='test'),
]
