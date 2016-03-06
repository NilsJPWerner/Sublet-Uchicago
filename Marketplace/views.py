from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from listings.models import Listing
from django.forms.models import model_to_dict
import json
from django.core.serializers.json import DjangoJSONEncoder


# Should limit the fields in this call to save space
def ajax_listing_search_data(request):
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
    for i in results:
        data = model_to_dict(i)
        photos = i.get_photos(4)
        photo_list = []
        for p in photos[1:]:
            photo_list.append(p.image.url)
        data["cover_photo"] = photos[0].image.url
        data["photos"] = photo_list
        listings.append(data)

    ret = json.dumps(listings, cls=DjangoJSONEncoder)
    return HttpResponse(ret, content_type='application/json')


def ajax_get_cover_photo(request):
    pk = request.GET.get('pk')
    listing = get_object_or_404(Listing, pk=pk, user=request.user)
    data = serializers.serialize('json', [listing.get_cover_photo()])
    return HttpResponse(data, content_type='application/json')

