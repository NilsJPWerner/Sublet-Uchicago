from django.http import HttpResponse
from .models import Listing


#Custom decorator
def listing_ownership(func):
    def check_and_call(request, *args, **kwargs):
        #user = request.user
        #print user.id
        listing_id = kwargs["listing_id"]
        listing = Listing.objects.get(id=listing_id)
        if not (listing.user.id == request.user.id):
            return HttpResponse("It is not yours ! You are not permitted !",
                        content_type="application/json", status=403)
        return func(request, *args, **kwargs)
    return check_and_call
