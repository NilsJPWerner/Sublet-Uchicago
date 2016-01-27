from django.http import HttpResponse
from django.utils.functional import wraps
from django.shortcuts import get_object_or_404
from .models import Listing


# Custom decorator
def listing_ownership(view):
    @wraps(view)
    def inner(request, listing_id, *args, **kwargs):
        listing = get_object_or_404(Listing, id=listing_id)
        if (listing.user.id != request.user.id):
            return HttpResponse("It is not yours ! You are not permitted !",
                        content_type="application/json", status=403)
        return view(request, listing, *args, **kwargs)
    return inner
