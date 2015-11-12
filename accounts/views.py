from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth, messages
from django.core.urlresolvers import reverse

from .forms import ListingForm
from .models import listing


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
                #seller_id=somecode,
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


def account_home(request):
    if request.user.is_authenticated():
        context = {}
        return render(request, 'account/home.html', context)
    else:
        return HttpResponseRedirect(reverse('account_login'))
        all_listings = listing.objects.all()

