from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

#Disclaimer: Our models are based on https://github.com/sczizzo/Dhaka/blob/develop/db/schema.rb
# Create your models here.


class listing(models.Model):
    description = models.CharField(null=False, max_length=300)
    details = models.TextField(null=False, max_length=2000)
    price = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    seller_id = models.OneToOneField(User) 
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    # permalink = models.CharField(blank=False, null=False, max_length=300)
    renewed_at = models.DateTimeField(auto_now=True, null=True)
    renewals = models.IntegerField(default=0)
    published = models.BooleanField(default=True)
    location = models.CharField(null=True, max_length=200)
    #added stuff
    slug = models.SlugField(max_length=300)


    def get_absolute_url(self):
        return reverse('accounts:display_listing', args=(self.slug,))

    def get_absolute_edit_url(self):
        return reverse('accounts:edit_listing', kwargs={'slug': self.slug})
        # return reverse('edit_listing', kwargs={'slug': self.slug,})


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


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, default="0", null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', default="/static/img/accounts/empty-photo.png", blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    uni_division = models.CharField(choices=UNI_DIV, max_length=50, blank=True)
    description = models.TextField(blank=True)


def user_post_save(sender, instance, created, **kwargs):
    """Create a user profile when a new user account is created"""
    if created == True:
        p = ExtendedUser()
        p.user = instance
        p.save()