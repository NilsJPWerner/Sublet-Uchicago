from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm

from .forms import ListingForm, ExtendedUserForm
from .models import listing, ExtendedUser


def add(request):
    # Check if User is logged in

    listingform = ListingForm(prefix='listingform')
    if request.method == 'GET':
        return render_to_response('add_listing.html', 
            locals(), context_instance=RequestContext(request))





    if request.method == 'POST':
        form = ListingForm(request.POST, prefix='listingform')
        if form.is_valid(): 
            cd = form.cleaned_data
            new = listing(
                description=cd['description'],
                details=cd['details'],
                price=cd['price'],
                # seller_id=somecode,
                location=cd['location'])
            new.save()
            return HttpResponseRedirect('/listing/' + str(new.id))
        else:
            #display more specific error message
            messages.warning(request, 'Your listing is invalid, please try again!')
            return HttpResponseRedirect('')


def get_listing(request, listing_id):
    listingObject = listing.objects.get(id=listing_id)
    return render_to_response('display_listing.html', 
        locals(), context_instance=RequestContext(request))

# Implement a method in the listing display page to only allow edit if you
# posted it to begin with
# def edit_listing(request):
#   if request.method == 'GET':
#       return render_to_response('edit_listing.html',
#           locals(), context_instance=RequestContext(request))
#   if request.method == 'POST':
#       # listingObject = request.sessions[***]

#       return HttpResponseRedirect('/listing/' + str(listingObject.id))


@login_required
def account_home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account/home.html', context)


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
            form = ExtendedUserForm(instance=u)  #No request.POST
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


