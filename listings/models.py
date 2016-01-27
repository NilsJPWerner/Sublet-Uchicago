from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from decimal import Decimal
from PIL import Image
import os


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


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Descrition
    name = models.CharField(max_length=40, blank=True)
    summary = models.TextField(max_length=400, blank=True)
    price = models.IntegerField(default=0, blank=True)

    # Location
    country = models.CharField(max_length=100, blank=True)  # Not used atm
    street_address = models.CharField(max_length=100, blank=True)
    apt = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=40, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal(41.796662))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal(-87.594183))

    # Details step
    bed_size = models.CharField(choices=BED_SIZE, max_length=10, blank=True)
    roommate_count = models.CharField(choices=ROOMMATES, max_length=5, blank=True)
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
    fall_quarter = models.BooleanField(default=False)
    winter_quarter = models.BooleanField(default=False)
    spring_quarter = models.BooleanField(default=False)
    summer_quarter = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    # Object meta data
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    published = models.BooleanField(default=False)

    def description_complete(self):
        if self.name and self.summary and self.price:
            return True
        return False

    def location_complete(self):
        if self.street_address and self.zip_code:
            return True
        return False

    def details_complete(self):
        if self.bed_size and self.roommate_count and self.bathroom:
            return True
        return False

    def photos_complete(self):
        if Photo.objects.filter(listing=self.id):
            return True
        return False

    def calendar_complete(self):
        if self.fall_quarter or self.winter_quarter or self.spring_quarter or self.summer_quarter:
            return True
        elif self.start_date and self.end_date:
            return True
        return False

    def listing_complete(self):
        if self.description_complete() and self.location_complete() and self.photos_complete() and self.details_complete() and self.calendar_complete():
            return True
        return False

    def steps_remaining(self):
        counter = 5
        if self.description_complete():
            counter -= 1
        if self.location_complete():
            counter -= 1
        if self.details_complete():
            counter -= 1
        if self.photos_complete():
            counter -= 1
        if self.calendar_complete():
            counter -= 1
        return counter

    def get_cover_photo(self):
        if self.photo_set.filter(is_cover_photo=True).count() > 0:
            return self.photo_set.filter(is_cover_photo=True)[0]
        elif self.photo_set.all().count() > 0:
            return self.photo_set.all()[0]
        else:
            return None


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

    def get_name(self):
        return os.path.basename(self.image.path)

    def get_size(self):
        size = self.image.size
        if size >= 1000000:
            return str(truncate(size/1000000, 2)) + " MB"
        else:
            return str(truncate(size/1000, 2)) + " KB"

    def get_delete_url(self):
        return reverse('listings:jfu_delete', kwargs={'pk': self.id})

    # def delete(self):
    #     try:
    #         os.remove(self.get_medium_filename())
    #         os.remove(self.get_small_filename())
    #     except:
    #         pass
    #     super(Photo, self).delete()


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

