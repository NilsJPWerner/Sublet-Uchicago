from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [

    url(r'^accounts/home/$', views.home, name='home'),
    url(r'^accounts/listings/$', views.your_listings, name='listings'),
    url(r'^accounts/starred_listings/$', views.starred_listings, name='starred_listings'),
    url(r'^accounts/edit_profile/$', views.edit_profile, name='edit_profile'),

    # Account verifications
    url(r'^accounts/verification/$',
        views.verification, name='verification'),
    url(r'^accounts/disconnect/(?P<service>[0-9A-Za-z]+)',
        views.disconnect_service, name='disconnect_service'),

    # Account settings
    url(r'^accounts/settings/$',
        login_required(views.settings.as_view()), name='settings'),
    url(r'^accounts/password_change_successful/$',
        TemplateView.as_view(template_name='account/password_change_successful.html'),
        name='password_change_successful'),
    url(r'^accounts/email_add_successful/$',
        login_required(views.email_add_successful.as_view()), name='email_add_successful'),
]
