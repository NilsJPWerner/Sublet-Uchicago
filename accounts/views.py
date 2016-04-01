from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib2


from .forms import ExtendedUserForm, ChangePasswordFormModified, AddEmailFormCombined
from .models import ExtendedUser
from listings.models import Listing

from allauth.account.views import (PasswordChangeView, EmailView, _ajax_response)
from allauth.account.adapter import get_adapter
from allauth.account import signals
from allauth.socialaccount.models import SocialAccount


@login_required
def home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account/home.html', context)


@login_required
def your_listings(request):
    user = request.user
    listings = Listing.objects.filter(user=user.id)
    context = {'user': user, 'listings': listings}
    return render(request, 'account/listings.html', context)


@login_required
def starred_listings(request):
    user = request.user
    listings = Listing.objects.filter(user=user.id)
    context = {'user': user, 'listings': listings}
    return render(request, 'account/starred_listings.html', context)


class verif(object):
    def __init__(self, name, link, disconnect_link, description):
        self.name = name
        self.link = link
        self.disconnect_link = disconnect_link
        self.description = description


@login_required
def verification(request):
    uchicago = verif('Uchicago E-mail',
        reverse('accounts:settings'),
        reverse('accounts:settings'),
        'Insert text about Uchicago E-mail account')
    # Django limitations forced me to hardcode the connect urls.
    # Not very DRY so might eventually fix
    facebook = verif('Facebook',
        '/accounts/facebook/login/?process=connect',
        reverse('accounts:disconnect_service', args=('facebook',)),
        'Insert text about facebook here')
    google = verif('Google',
        '/accounts/google/login/?process=connect&next=%2Faccounts%2Fverification%2F',
        reverse('accounts:disconnect_service', args=('google',)),
        'Insert text about google here')
    linkedin = verif('Linkedin',
        '/accounts/linkedin/login/?process=connect&next=%2Faccounts%2Fverification%2F',
        reverse('accounts:disconnect_service', args=('linkedin',)),
        'Insert text about linkedin here')

    verified_list = []
    unverified_list = [uchicago, facebook, google, linkedin]

    if (request.user.extendeduser.uchicago_email()):
        unverified_list.remove(uchicago)
        verified_list.append(uchicago)
    if (request.user.extendeduser.social_account('facebook')):
        verified_list.append(facebook)
        unverified_list.remove(facebook)
    if (request.user.extendeduser.social_account('google')):
        verified_list.append(google)
        unverified_list.remove(google)
    if (request.user.extendeduser.social_account('linkedin')):
        verified_list.append(linkedin)
        unverified_list.remove(linkedin)

    context = {'user': request.user, 'verified': verified_list, 'unverified': unverified_list}
    return render(request, 'account/verification.html', context)


@login_required
def disconnect_service(request, service):
    # Should really use a POST request to disconnect rather than a get
    if service in ('facebook', 'google', 'linkedin'):
        try:
            account = SocialAccount.objects.get(user=request.user, provider=service)
            account.delete()
            return HttpResponseRedirect(reverse('accounts:verification'))
        except:
            raise Http404("There has been error with disconnecting your account")
    else:
        raise Http404("The urls are messed up")


@login_required
def edit_profile(request):
    if request.method == "POST":
        u = ExtendedUser.objects.get(user=request.user)
        form = ExtendedUserForm(request.POST, request.FILES, instance=u)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            return HttpResponseRedirect(reverse('accounts:edit_profile'))
    else:
        try:
            u = ExtendedUser.objects.get(user=request.user)
            form = ExtendedUserForm(instance=u)  # No request.POST
        except ObjectDoesNotExist:
            form = ExtendedUserForm(request.FILES)

    context = {'form': form, 'user': request.user}
    return render(request, 'account/edit_profile.html', context)


@login_required
def ajax_fb_photo(request):
    if request.method == "POST":
        try:
            fb = SocialAccount.objects.get(user=request.user, provider="facebook")
            url = fb.get_avatar_url()
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(url).read())
            img_temp.flush()
            file_name = "profile_picture_" + str(request.user.id)
            request.user.extendeduser.profile_picture.save(file_name, File(img_temp))
            img_temp.close()
            return HttpResponse(request.user.extendeduser.profile_picture.url)
        except:
            return HttpResponse("not_logged_in")
    else:
        return HttpResponseBadRequest


class settings(PasswordChangeView):
    template_name = "account/settings.html"
    form_class = ChangePasswordFormModified
    success_url = reverse_lazy('accounts:settings')

    def get_context_data(self, **kwargs):
        ret = super(PasswordChangeView, self).get_context_data(**kwargs)
        # NOTE: For backwards compatibility
        ret['password_change_form'] = ret.get('form')
        ret['email_form'] = AddEmailFormCombined()
        # (end NOTE)
        return ret


class email_add_successful(EmailView):
    success_url = reverse_lazy('accounts:settings')
    form_class = AddEmailFormCombined

    def form_valid(self, form):
        email_address = form.save(self.request)
        get_adapter().add_message(self.request,
                                  messages.INFO,
                                  'account/messages/'
                                  'email_confirmation_sent.txt',
                                  {'add_email': form.cleaned_data["add_email"]})
        signals.email_added.send(sender=self.request.user.__class__,
                                 request=self.request,
                                 user=self.request.user,
                                 email_address=email_address)
        return super(EmailView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        res = None
        if "action_add" in request.POST:
            res = super(EmailView, self).post(request, *args, **kwargs)
        elif request.POST.get("email"):
            if "action_send" in request.POST:
                res = self._action_send(request)
            elif "action_remove" in request.POST:
                res = self._action_remove(request)
            elif "action_primary" in request.POST:
                res = self._action_primary(request)
            res = res or HttpResponseRedirect(reverse('accounts:settings'))
            # Given that we bypassed AjaxCapableProcessFormViewMixin,
            # we'll have to call invoke it manually...
            res = _ajax_response(request, res)
        else:
            # No email address selected
            res = HttpResponseRedirect(reverse('accounts:settings'))
            res = _ajax_response(request, res)
        return res
