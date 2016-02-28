from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core import serializers
from listings.models import Listing


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

    # Filter by quarters first
    if (not fall) and (not winter) and (not spring) and (not summer):
        results = Listing.objects.filter(published=True)
    else:
        results = Listing.objects.filter(published=True,
            fall_quarter=fall, winter_quarter=winter,
            spring_quarter=spring, summer_quarter=summer)

    if bathroom != "none":
        results = results.filter(bathroom=bathroom)
    results = results.filter(bed_size__gte=bedsize)
    # Price filtering
    results = results.filter(price__gte=price_low, price__lte=price_high)

    # .order_by('username')
    context = {'results': results}
    return render(request, 'Marketplace/results.html', context)


def ajax_listing_search_coordinates(request):
    results = Listing.objects.filter(published=True)
    data = serializers.serialize('json', results)
    return HttpResponse(data, content_type='application/json')
