import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .utility import listing_ownership
from .models import Listing, Photo
from .forms import EditDescriptionForm, EditDetailsForm, EditLocationForm, EditCalendarForm
from jfu.http import upload_receive, UploadResponse, JFUResponse


@login_required
def add_listing(request):
    new_listing = Listing(user=request.user)
    new_listing.save()
    return HttpResponseRedirect(reverse('listings:edit_listing_description', args=(new_listing.id,)))


@login_required
def edit_listing(request, listing_id):
    return HttpResponseRedirect(reverse('listings:edit_listing_description', args=(listing_id,)))


# Change these form views to one class
@login_required
@listing_ownership
def edit_listing_description(request, listing):
    if request.method == "POST":
        form = EditDescriptionForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listings:edit_listing_location', args=(listing.id,)))
    else:
        form = EditDescriptionForm(instance=listing)
    context = {'form': form, 'user': request.user, 'listing': listing}
    return render(request, 'listing/edit_listing_description.html', context)


@login_required
@listing_ownership
def edit_listing_location(request, listing):
    if request.method == "POST":
        form = EditLocationForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listings:edit_listing_details', args=(listing.id,)))
    else:
        form = EditLocationForm(instance=listing)
    context = {'form': form, 'user': request.user, 'listing': listing}
    return render(request, 'listing/edit_listing_location.html', context)


@login_required
@listing_ownership
def edit_listing_details(request, listing):
    if request.method == "POST":
        form = EditDetailsForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listings:edit_listing_photos', args=(listing.id,)))
    else:
        form = EditDetailsForm(instance=listing)
    context = {'form': form, 'user': request.user, 'listing': listing}
    return render(request, 'listing/edit_listing_details.html', context)


@login_required
@listing_ownership
def edit_listing_calendar(request, listing):
    if request.method == "POST":
        form = EditCalendarForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listings:edit_listing_calendar', args=(listing.id,)))
    else:
        form = EditCalendarForm(instance=listing)
    context = {'form': form, 'user': request.user, 'listing': listing}
    return render(request, 'listing/edit_listing_calendar.html', context)


@login_required
@listing_ownership
def edit_listing_photos(request, listing):
    photos = Photo.objects.filter(listing=listing.id)
    context = {'accepted_mime_types': 'image/*', 'listing': listing, 'photos': photos}
    return render(request, 'listing/edit_listing_photos.html', context)


@login_required
@require_POST
def upload(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id, user=request.user)

    image = upload_receive(request)

    instance = Photo(image=image, listing=listing)
    instance.save()
    basename = os.path.basename(instance.image.path)

    file_dict = {
        'name': basename,
        'size': image.size,

        'url': instance.image.url,
        'thumbnailUrl': instance.image.url,

        'deleteUrl': reverse('listings:jfu_delete', kwargs={'pk': instance.pk}),
        'deleteType': 'POST',
    }
    return UploadResponse(request, file_dict)


@login_required
@require_POST
def upload_delete(request, pk):
    success = True
    try:
        instance = Photo.objects.get(pk=pk)
        if instance.listing.user != request.user:
            success = False
            return JFUResponse(request, success)
        instance.delete()
    except Photo.DoesNotExist:
        success = False
    return JFUResponse(request, success)


@login_required
@listing_ownership
def publish_listing(request, listing):
    if (listing.listing_complete()):
        listing.published = True
        listing.save()
        return HttpResponseRedirect(reverse("accounts:listings"))
    else:
        # In case someone is sneaky and tries to publish before complete
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Need to make the listing automatically unpublish if it is incomplete
@login_required
@listing_ownership
def unpublish_listing(request, listing):
    listing.published = False
    listing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@listing_ownership
def delete_listing(request, listing):
    listing.delete()
    return HttpResponseRedirect(reverse("accounts:listings"))
