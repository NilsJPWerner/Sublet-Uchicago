from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from listings.models import Listing


def ajax_listing_search(request):
    bathroom = request.GET.get('q')
    if bathroom is not None:
        results = Listing.objects.filter(
            bathroom=bathroom)   # .order_by('username')
        context = {'results': results}
        return render(request, 'Marketplace/results.html', context)
