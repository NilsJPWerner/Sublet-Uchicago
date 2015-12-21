from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    # url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add, name='New Listing'),
    url(r'^listing/(?P<listing_id>.*)$', views.get_listing, name='Display Listing'),
    url(r'^accounts/home/$', views.account_home, name='account_home'),
    url(r'^accounts/verification/$', views.account_verification, name='account_verification'),
    url(r'^accounts/edit_profile/$', views.account_edit_profile, name='account_edit_profile'),
    url(r'^accounts/settings/$', views.account_settings, name='account_settings'),
    url(r'^accounts/password_change_successful/$', 
      TemplateView.as_view(template_name='account/password_change_successful.html'),
      name='password_change_successful'),
]
