import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache

from listings.models import Listing
from forms import ListingForm, ListingFormAuthenticated


@never_cache
def search(request):

    if request.is_ajax():
        quarter     = request.GET.get('quarter')
        bedsize     = request.GET.get('bedsize')
        bathroom    = request.GET.get('bathroom')
        roommates   = request.GET.get('roommates')
        price_low   = request.GET.get('price_low')
        price_high  = int(request.GET.get('price_high'))
        page        = request.GET.get('page')
        per_page    = 2  #request.GET.get('per_page')

        # Price filtering
        results = Listing.objects.filter(price__gte=price_low)
        if price_high < 1500:
            results = Listing.objects.filter(price__lte=price_high)

        # Only published listings
        results = results.filter(published=True)

        # Filter by quarters
        if quarter == 'fall':
             results = results.filter(fall_quarter=True)
        elif quarter == 'winter':
            results = results.filter(winter_quarter=True)
        elif quarter == 'spring':
            results = results.filter(spring_quarter=True)
        elif quarter == 'summer':
            results = results.filter(summer_quarter=True)
        else:
            pass  # if no quarter, select all

        if bedsize and bedsize != 'any':
            results = results.filter(bed_size__gte=bedsize)

        if bathroom and bathroom != 'any':
            results = results.filter(bathroom=bathroom)

        if roommates and roommates != 'any':
            results = results.filter(roommate_count=roommates)

        paginator = Paginator(results, per_page)
        try:
            listings = paginator.page(page)
            current_page = page
        except PageNotAnInteger:
            listings = paginator.page(1)
            current_page = 1
        except EmptyPage:
            listings = paginator.page(paginator.num_pages)
            current_page = paginator.num_pages

        response = {'listings': [], 'pages': paginator.num_pages, 'current_page': current_page}

        for listing in listings:
            # Convert each instance into a dict including only needed fields
            data = model_to_dict(listing, fields=["name", "id", "latitude", "longitude", "summary", "price"])
            photos = listing.get_photos(5)
            data["cover_photo"] = photos[0].image_s.url  # Split photos for lazy loading
            data["photos"] = [p.image_s.url for p in photos[1:]]
            data["listing_url"] = listing.get_absolute_url()
            data["username"] = listing.user.extendeduser.first_name + " " + listing.user.extendeduser.last_name
            data["user_url"] = listing.get_user_url()
            if request.user.is_authenticated():
                data["starred"] = listing.extendeduser_set.filter(id=request.user.extendeduser.id).exists()

            response['listings'].append(data)

        ret = json.dumps(response, cls=DjangoJSONEncoder)
        return HttpResponse(ret, content_type='application/json')

    else:
        return render(request, "sublet/search.html", {})


# Toggle whether the listing is starred by the user or not.
def ajax_star(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            listing_id = request.POST.get("listing")
            listing = get_object_or_404(Listing, id=listing_id)
            if (request.user.extendeduser.is_starred(listing_id)):
                request.user.extendeduser.starred.remove(listing)
                return HttpResponse("False")
            else:
                request.user.extendeduser.starred.add(listing)
                return HttpResponse("True")
        else:
            return HttpResponse(reverse("account_login"))
    else:
        return HttpResponseBadRequest


def public_profile(request, user):
    u = get_object_or_404(User, pk=user)
    verified, unverified = u.extendeduser.get_verifications()
    context = {'user': u, 'verified': verified, 'unverified': unverified}
    return render(request, 'sublet/public_profile.html', context)


def listing(request, listing):
    if request.user.is_authenticated():
        form = ListingFormAuthenticated(request.POST or None)
    else:
        form = ListingForm(request.POST or None)
    l = get_object_or_404(Listing, pk=listing)
    starred = ""
    if request.user.is_authenticated() and l.extendeduser_set.filter(
            id=request.user.extendeduser.id).exists():
        starred = "starred"
    if request.method == "POST":
        if form.is_valid():
            if request.user.is_authenticated():
                address = request.user.extendeduser.get_primary_email()
            else:
                address = form.cleaned_data['email']
            message = form.cleaned_data["message"]
            recipient = [l.user.extendeduser.get_primary_email(), ]
            email = EmailMessage("Listing inquiry", message, address,
                recipient, headers={'From': address})
            email.send()

    context = {"listing": l, "starred": starred, "form": form}
    return render(request, 'sublet/listing.html', context)


# Should probably clean and validate this stuff
def ajax_bug_report(request):
    if request.method == "POST":
        address = request.POST.get("email")
        report = request.POST.get("report")
        contactme = request.POST.get("contactme")

        recipients = ['nils.jp.werner@gmail.com', ]
        header = "Bug report | contact me: " + contactme
        email = EmailMessage(header, report, 'nils.jp.werner@gmail.com',
            recipients, headers={'From': address})
        email.send()
        return HttpResponse("Success!")
    else:
        return HttpResponseBadRequest


def ajax_contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        recipients = ['nils.jp.werner@gmail.com', ]
        header = subject + ' from: ' + name
        email = EmailMessage(header, message, 'nils.jp.werner@gmail.com',
            recipients, headers={'From': address})
        email.send()
        return HttpResponse("Success!")
    else:
        return HttpResponseBadRequest
