from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm
from django.template.defaultfilters import slugify

from .forms import ListingForm, ExtendedUserForm
from .models import listing, ExtendedUser
from allauth.account.views import EmailView, _ajax_response


def add(request):
    # Check if User is logged in
    # if not request.user.is_authenticated():
    #     messages.warning(request, 'Please login to add a listing!')
    #     return HttpResponseRedirect('/accounts/home')

    listingform = ListingForm(prefix='listingform')
    if request.method == 'GET':
        return render_to_response('add_listing.html', 
            locals(), context_instance=RequestContext(request))





    if request.method == 'POST':
        form = ListingForm(request.POST, prefix='listingform')
        if form.is_valid(): 
            cd = form.cleaned_data
            inputSlug = slugify(cd['description'])
            new = listing(
                description=cd['description'],
                details=cd['details'],
                price=cd['price'],
                seller_id=request.user,
                slug=inputSlug,
                location=cd['location'])
            new.save()
            return HttpResponseRedirect('/listing/' + inputSlug)
        else: 
            #display more specific error message
            messages.warning(request, 'Your listing is invalid, please try again!')
            return HttpResponseRedirect('')


def get_listing(request, slug):
    listingObject = listing.objects.get(slug=slug)
    listing_id = listingObject.id
    print listingObject.get_absolute_edit_url()
    if request.user.id == listing_id:
      same_user_as_post = True
    else:
      same_user_as_post = False
    return render_to_response('display_listing.html', 
        locals(), context_instance=RequestContext(request))


# Implement a method in the listing display page to only allow edit if you
# posted it to begin with
def edit_listing(request, slug):
    listingObject = listing.objects.get(slug=slug)
    listing_id = listingObject.id

    if request.user.id == listing_id:
      same_user_as_post = True
    else:
      same_user_as_post = False
      messages.warning(request, 'You can only edit your own posts!')
      return HttpResponseRedirect('')


    if request.method == 'GET':
        listingform = ListingForm(instance=listingObject, prefix='listingform')
        return render_to_response('edit_listing.html',
            locals(), context_instance=RequestContext(request))



    if request.method == 'POST':
        listingform = ListingForm(request.POST, prefix='listingform')
        #Check if data is valid & then modify it
        if listingform.is_valid():
            cd = listingform.cleaned_data
            listingObject.description = cd['description']
            listingObject.details= cd['details']
            listingObject.price = cd['price']
            listingObject.location=cd['location']
            listingObject.renewals += 1
        listingObject.save()
        return HttpResponseRedirect('/listing/' + listingObject.slug)


@login_required
def account_home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account/home.html', context)

class verification(object):
    """docstring for verification"""
    def __init__(self, name, link, description, type):
        self.name = name
        self.description = description
        if type == 'allauth':
            self.link = '{% provider_login_url "' + link + '" process="connect" %}'
        elif type == 'other':
            self.link = '{% url ' + link + ' %}'
        else:
            self.link = ''


@login_required
def account_verification(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account/verification.html', context)


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


@login_required
def account_settings(request):
    password_change_form = PasswordChangeForm
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:password_change_successful'))
    else:
        form = password_change_form(user=request.user)
    context = {'form': form, 'user': request.user}
    return render(request, 'account/settings.html', context)









class test(EmailView):
    template_name = 'account/email.html'
    password_change_form = PasswordChangeForm
    print "just chillin"

    def post(self, request, *args, **kwargs):
        print "posting"
        res = None
        if "action_add" in request.POST:
            res = super(EmailView, self).post(request, *args, **kwargs)
        # Added form condition for password change
        elif request.POST.get("email"):
            if "action_send" in request.POST:
                res = self._action_send(request)
            elif "action_remove" in request.POST:
                res = self._action_remove(request)
            elif "action_primary" in request.POST:
                res = self._action_primary(request)
            res = res or HttpResponseRedirect(reverse('account_email'))
            # Given that we bypassed AjaxCapableProcessFormViewMixin,
            # we'll have to call invoke it manually...
            res = _ajax_response(request, res)
        else:
            # No email address selected
            res = HttpResponseRedirect(reverse('account_email'))
            res = _ajax_response(request, res)
        return res

    def password_change(self, request, *args, **kwargs):
        print "got to the function"
        self.password_change_form = self.password_change_form(user=request.user, data=request.POST)
        if self.password_change_form.is_valid():
            self.password_change_form.save()
            return HttpResponseRedirect(reverse('accounts:password_change_successful'))

    def get_context_data(self, **kwargs):
        print 'poop'
        ret = super(EmailView, self).get_context_data(**kwargs)
        # NOTE: For backwards compatibility
        ret['add_email_form'] = ret.get('form')
        ret['passwordform'] = self.password_change_form(user=self.request.user)
        # (end NOTE)
        return ret

@login_required
def password_change_post(request):
    password_change_form = PasswordChangeForm
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:password_change_successful'))

