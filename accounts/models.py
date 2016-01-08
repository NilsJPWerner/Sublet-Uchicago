from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from decimal import Decimal
from PIL import Image
import os

#Disclaimer: Our models are based on https://github.com/sczizzo/Dhaka/blob/develop/db/schema.rb
# Create your models here.


# class images(models.Model):
#   listing_id = models.IntegerField(null=False) #Maybe implement as foreignkey?
#   created_at = models.DateTimeField(auto_now_add=True, null=False)
#   updated_at = models.DateTimeField(auto_now=True, auto_now_add=True, null=False)
#   photo_file_name = models.CharField(max_length=150)
#   photo_content_type = models.CharField(max_length=20)
#   photo_file_size = models.IntegerField(null=False)

UNI_DIV = (('NA', 'Not Affiliated'),
    ('first', 'First Year'),
    ('second', 'Second Year'),
    ('third', 'Third Year'),
    ('fourth', 'Fourth Year'),
    ('grad', 'Graduate Student'),
    ('faculty', 'Faculty Member'),
    ('other', 'Other division'))

ROOMMATES = (('0', '0'), ('1', '1'),
            ('2', '2'), ('3', '3'),
            ('4', '4'), ('5+', '5+'))

BED_SIZE = (('king', 'King'),
    ('queen', 'Queen'),
    ('full', 'Full'),
    ('twin', 'Twin'))

BATHROOM = (('shared', 'Shared'),
    ('private', 'Private'))

YESNO = (('yes', 'Yes'), ('no', 'No'))

QUARTER = (('summer', 'Summer'),
    ('fall', 'Fall'),
    ('winter', 'Winter'),
    ('spring', 'Spring'))


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, default="0", null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures',
        default="/static/img/accounts/empty-photo.png", blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    uni_division = models.CharField(choices=UNI_DIV, max_length=50, blank=True)
    description = models.TextField(blank=True)


def user_post_save(sender, instance, created, **kwargs):
    # Create a user profile when a new user account is created
    if created:
        p = ExtendedUser()
        p.user = instance
        p.save()


class Listing(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # Blank is temporary, need to add a method to allow blank save
    # but then require it to be published

    # Descrition
    listing_name = models.CharField(max_length=40, blank=True)
    summary = models.TextField(max_length=400, blank=True)

    # Location
    address = models.CharField(max_length=100, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal(41.796662))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal(-87.594183))

    # Details step
    bed_size = models.CharField(choices=BED_SIZE, max_length=10, blank=True)
    roomate_count = models.CharField(choices=ROOMMATES, max_length=5, blank=True)
    bathroom = models.CharField(choices=BATHROOM, max_length=10, blank=True)
    ac = models.BooleanField(default=False)
    in_unit_washer_dryer = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    cable_tv = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    wheel_chair_accessible = models.BooleanField(default=False)
    pets_live_here = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)

    # Calendar
    quarter = models.CharField(choices=QUARTER, max_length=10, blank=True)

    # Price 
    price = models.IntegerField(default=0, blank=True)
    amenities_included = models.CharField(choices=YESNO, max_length=10, blank=True)
    amenities_price = models.IntegerField(default=0, blank=True)
    prefered_payment_method = models.CharField(max_length=20, blank=True)

    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    # permalink = models.CharField(blank=False, null=False, max_length=300)
    renewed_at = models.DateTimeField(auto_now=True, null=True)
    renewals = models.IntegerField(default=0)
    published = models.BooleanField(default=True)
    #added stuff
    slug = models.SlugField(max_length=300)

    def description_complete(self):
        if self.listing_name and self.summary:
            return True
        return False

    def location_complete(self):
        if self.address and self.zip_code:
            return True
        return False

    def details_complete(self):
        if self.bed_size and self.roomate_count and self.bathroom:
            return True
        return False

    # photos complete

    def calendar_complete(self):
        if self.quarter:
            return True
        return False

    def price_complete(self):
        if self.price and self.amenities_included and self.prefered_payment_method:
            if self.amenities_included == 'no' and not self.amenities_price:
                return False
            return True
        return False

    def listing_complete(self):
        if self.description_complete() and self.location_complete() and self.details_complete() and self.calendar_complete() and self.price_complete():
            return True
        return False

    def get_cover_photo(self):
        if self.photo_set.filter(is_cover_photo=True).count() > 0:
            return self.photo_set.filter(is_cover_photo=True)[0]
        elif self.photo_set.all().count() > 0:
            return self.photo_set.all()[0]
        else:
            return None

    # def get_absolute_url(self):
    #     return reverse('accounts:display_listing', args=(self.slug,))

    # def get_absolute_edit_url(self):
    #     return reverse('accounts:edit_listing', kwargs={'slug': self.slug})
    #     # return reverse('edit_listing', kwargs={'slug': self.slug,})


class Photo(models.Model):
    listing = models.ForeignKey(Listing, null=True)
    image = models.ImageField(upload_to='listing_photos/%Y/%m/%d', null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    is_cover_photo = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # # Maybe add something that renames the file to something standard
    # # Maybe also resize original image to something more sane 
    # def save(self):
    #     if self.is_cover_photo:
    #         other_cover_photos = Photo.objects.filter(album=self.album, is_cover_photo=True)
    #         for photo in other_cover_photos:
    #             photo.is_cover_photo = False
    #             photo.save()
    #     filename = self.filename
    #     if filename != '':
    #         image = Image.open(filename)

    #         # need to add PNG conversion
    #         # if image.mode != 'RGB':
    #         #     image = image.convert('RGB')

    #         size_large = (image[0]/image[1] * 800, 800)
    #         image.thumbnail(size_large, Image.BICUBIC)
    #         image.save(self.get_large_filename())

    #         size_medium = (200, image[1]/image[0]*200)
    #         image.thumbnail(size_medium, Image.BICUBIC)
    #         image.save(self.get_medium_filename())

    #         size_small = (image[0]/image[1] * 80, 80)
    #         image.thumbnail(size_small, Image.BICUBIC)
    #         image.save(self.get_small_filename())
    #     super(Photo, self).save()

    def get_large_filename(self):
        return 'l_' + self.filename

    def get_medium_filename(self):
        return 'm_' + self.filename

    def get_small_filename(self):
        return 's_' + self.filename

    # def delete(self):
    #     try:
    #         os.remove(self.get_medium_filename())
    #         os.remove(self.get_small_filename())
    #     except:
    #         pass
    #     super(Photo, self).delete()



