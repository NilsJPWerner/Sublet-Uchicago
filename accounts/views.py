from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify

from .forms import (ListingForm, ExtendedUserForm,
                    ChangePasswordFormModified, AddEmailFormCombined,
                    EditDescriptionForm, )
from .models import Listing, ExtendedUser
from allauth.account.views import (PasswordChangeView, EmailView,
                                    _ajax_response)
from allauth.account.adapter import get_adapter
from allauth.account import signals
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount


# def add(request):
#     # Check if User is logged in
#     # if not request.user.is_authenticated():
#     #     messages.warning(request, 'Please login to add a listing!')
#     #     return HttpResponseRedirect('/accounts/home')

#     listingform = ListingForm(prefix='listingform')
#     if request.method == 'GET':
#         return render_to_response('add_listing.html', 
#             locals(), context_instance=RequestContext(request))



#     if request.method == 'POST':
#         form = ListingForm(request.POST, prefix='listingform')
#         if form.is_valid(): 
#             cd = form.cleaned_data
#             inputSlug = slugify(cd['description'])
#             new = listing(
#                 description=cd['description'],
#                 details=cd['details'],
#                 price=cd['price'],
#                 seller_id=request.user,
#                 slug=inputSlug,
#                 location=cd['location'])
#             new.save()
#             return HttpResponseRedirect('/listing/' + inputSlug)
#         else: 
#             #display more specific error message
#             messages.warning(request, 'Your listing is invalid, please try again!')
#             return HttpResponseRedirect('')


# def get_listing(request, slug):
#     listingObject = listing.objects.get(slug=slug)
#     listing_id = listingObject.id
#     print listingObject.get_absolute_edit_url()
#     if request.user.id == listing_id:
#       same_user_as_post = True
#     else:
#       same_user_as_post = False
#     return render_to_response('display_listing.html', 
#         locals(), context_instance=RequestContext(request))


# # Implement a method in the listing display page to only allow edit if you
# # posted it to begin with
# def edit_listing(request, slug):
#     listingObject = listing.objects.get(slug=slug)
#     listing_id = listingObject.id

#     if request.user.id == listing_id:
#       same_user_as_post = True
#     else:
#       same_user_as_post = False
#       messages.warning(request, 'You can only edit your own posts!')
#       return HttpResponseRedirect('')


#     if request.method == 'GET':
#         listingform = ListingForm(instance=listingObject, prefix='listingform')
#         return render_to_response('edit_listing.html',
#             locals(), context_instance=RequestContext(request))



#     if request.method == 'POST':
#         listingform = ListingForm(request.POST, prefix='listingform')
#         #Check if data is valid & then modify it
#         if listingform.is_valid():
#             cd = listingform.cleaned_data
#             listingObject.description = cd['description']
#             listingObject.details= cd['details']
#             listingObject.price = cd['price']
#             listingObject.location=cd['location']
#             listingObject.renewals += 1
#         listingObject.save()
#         return HttpResponseRedirect('/listing/' + listingObject.slug)


@login_required
def account_home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account/home.html', context)


@login_required
def add_listing(request):
    new_listing = Listing(seller_id=request.user)
    new_listing.save()
    return HttpResponseRedirect(reverse('accounts:edit_listing_description', args=(new_listing.id,)))


@login_required
def edit_listing_description(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id=listing_id)
        form = EditDescriptionForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:edit_listing_details'))
    else:
        listing = get_object_or_404(Listing, id=listing_id)
        if listing.seller_id != request.user:
            # Make this a little better
            return HttpResponse("This is not yours")
        else:
            form = EditDescriptionForm(instance=listing)

    context = {'form': form, 'user': request.user}
    return render(request, 'listing/edit_listing_description.html', context)


@login_required
def edit_listing_details(request, listing_id):
    return HttpResponse("Thhings are coming")


class verification(object):
    """docstring for verification"""
    def __init__(self, name, link, disconnect_link, description):
        self.name = name
        self.link = link
        self.disconnect_link = disconnect_link
        self.description = description


@login_required
def account_verification(request):
    uchicago = verification('Uchicago E-mail',
        reverse('accounts:account_settings'),
        reverse('accounts:account_settings'),
        'Insert text about Uchicago E-mail account')
    # Django limitations forced me to hardcode the connect urls.
    # Not very DRY so might eventually fix
    facebook = verification('Facebook',
        '/accounts/facebook/login/?process=connect',
        reverse('accounts:account_disconnect_service', args=('facebook',)),
        'Insert text about facebook here')
    google = verification('Google',
        '/accounts/google/login/?process=connect&next=%2Faccounts%2Fverification%2F',
        reverse('accounts:account_disconnect_service', args=('google',)),
        'Insert text about google here')
    linkedin = verification('Linkedin',
        '/accounts/linkedin/login/?process=connect&next=%2Faccounts%2Fverification%2F',
        reverse('accounts:account_disconnect_service', args=('linkedin',)),
        'Insert text about linkedin here')

    verified_list = []
    unverified_list = [uchicago, facebook, google, linkedin]

    email_list = EmailAddress.objects.filter(user=request.user, verified=True)
    for email in email_list:
        if '@uchicago.edu' in email.email:
            unverified_list.remove(uchicago)
            verified_list.append(uchicago)
            break
    account_list = SocialAccount.objects.filter(user=request.user)
    for account in account_list:
        if account.provider == 'facebook':
            verified_list.append(facebook)
            unverified_list.remove(facebook)
        elif account.provider == 'google':
            verified_list.append(google)
            unverified_list.remove(google)
        elif account.provider == 'linkedin':
            verified_list.append(linkedin)
            unverified_list.remove(linkedin)
    context = {'user': request.user, 'verified': verified_list,
                'unverified': unverified_list}
    return render(request, 'account/verification.html', context)


@login_required
def account_disconnect_service(request, service):
    # Should really use a POST request to disconnect rather than a get
    if service in ('facebook', 'google', 'linkedin'):
        try:
            account = SocialAccount.objects.get(user=request.user, provider=service)
            account.delete()
            return HttpResponseRedirect(reverse('accounts:account_verification'))
        except:
            raise Http404("There has been error with disconnecting your account")
    else:
        raise Http404("The urls are messed up")


@login_required
def account_edit_profile(request):
    if request.method == "POST":
        u = ExtendedUser.objects.get(user=request.user)
        form = ExtendedUserForm(request.POST, request.FILES, instance=u)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            return HttpResponseRedirect(reverse('accounts:account_home'))
    else:
        try:
            u = ExtendedUser.objects.get(user=request.user)
            form = ExtendedUserForm(instance=u)  # No request.POST
        except ObjectDoesNotExist:
            form = ExtendedUserForm(request.FILES)

    context = {'form': form, 'user': request.user}
    return render(request, 'account/edit_profile.html', context)


class account_settings(PasswordChangeView):
    template_name = "account/settings.html"
    form_class = ChangePasswordFormModified
    success_url = reverse_lazy('accounts:account_settings')

    def get_context_data(self, **kwargs):
        ret = super(PasswordChangeView, self).get_context_data(**kwargs)
        # NOTE: For backwards compatibility
        ret['password_change_form'] = ret.get('form')
        ret['email_form'] = AddEmailFormCombined()
        # (end NOTE)
        return ret


class email_add_successful(EmailView):
    success_url = reverse_lazy('accounts:account_settings')
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
            res = res or HttpResponseRedirect(reverse('accounts:account_settings'))
            # Given that we bypassed AjaxCapableProcessFormViewMixin,
            # we'll have to call invoke it manually...
            res = _ajax_response(request, res)
        else:
            # No email address selected
            res = HttpResponseRedirect(reverse('accounts:account_settings'))
            res = _ajax_response(request, res)
        return res
