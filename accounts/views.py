from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.template.defaultfilters import slugify

from .forms import ListingForm
from .models import listing


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


def account_home(request):
    if request.user.is_authenticated():
        context = {}
        return render(request, 'account/home.html', context)
    else:
        return HttpResponseRedirect(reverse('account_login'))
        all_listings = listing.objects.all()

