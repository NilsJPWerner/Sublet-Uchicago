from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.cache import never_cache

from listings.models import Listing
from django.contrib.auth.models import User


@never_cache
def search(request):

    if request.is_ajax():

        bedsize = request.GET.get('bedsize')
        bathroom = request.GET.get('bathroom')
        # Javscript passes boolean in lowercase :( Sorry for the
        # ugly code it is a workaround
        fall = (request.GET.get('fall') == 'true')
        winter = (request.GET.get('winter') == 'true')
        spring = (request.GET.get('spring') == 'true')
        summer = (request.GET.get('summer') == 'true')
        price_low = (request.GET.get('price_low'))
        price_high = int(request.GET.get('price_high'))

        # Price filtering
        results = Listing.objects.defer("summary", "street_address",).filter(price__gte=price_low, price__lte=price_high)

        # Filter by quarters
        if (not fall) and (not winter) and (not spring) and (not summer):
            results = results.filter(published=True)
        else:
            results = results.filter(published=True,
                fall_quarter=fall, winter_quarter=winter,
                spring_quarter=spring, summer_quarter=summer)

        if bathroom != "none":
            results = results.filter(bathroom=bathroom)

        results = results.filter(bed_size__gte=bedsize)

        listings = []
        # Go through each lisitng in result and add photos and user
        for i in results:
            # Convert each instance into a dict including only needed fields
            data = model_to_dict(i, fields=["name", "id", "latitude", "longitude", "summary", "price"])

            # Should add a way to get small photos as an option
            photos = i.get_photos(5)
            photo_list = []

            # I split up the photos into cover photo and photos so that
            # all photos except cover photo can be set up to use lazy loading
            for p in photos[1:]:
                photo_list.append(p.image.url)
            data["cover_photo"] = photos[0].image.url
            data["photos"] = photo_list

            # get username and url to profile
            data["username"] = i.user.extendeduser.first_name + " " + i.user.extendeduser.last_name
            data["user_url"] = i.user.extendeduser.get_absolute_url()

            # Check if listing is starred by user if user is logged in
            if request.user.is_authenticated():
                data["starred"] = i.extendeduser_set.filter(id=request.user.extendeduser.id).exists()
            listings.append(data)

        ret = json.dumps(listings, cls=DjangoJSONEncoder)
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
    v = [("Email Address", "Verified")]
    uv = []
    if (u.extendeduser.uchicago_email()):
        v.append(("UChicago Email", "Verified"))
    else:
        uv.append(("UChicago Email", "Not Verified"))

    if (request.user.extendeduser.social_account('facebook')):
        v.append(("Facebook", "Connected"))
    else:
        uv.append(("Facebook", "Not Connected"))

    if (request.user.extendeduser.social_account('google')):
        v.append(("Google", "Connected"))
    else:
        uv.append(("Google", "Not Connected"))

    if (request.user.extendeduser.social_account('linkedin')):
        v.append(("Linkedin", "Connected"))
    else:
        uv.append(("Linkedin", "Not Connected"))

    context = {'user': u, 'verified': v, 'unverified': uv}
    return render(request, 'sublet/public_profile.html', context)
