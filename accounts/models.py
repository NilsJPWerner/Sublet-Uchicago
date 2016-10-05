from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from listings.models import Listing


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
    profile_picture = models.ImageField(upload_to='profile_pictures',
        default="/static/img/accounts/empty-photo.png", blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    uni_division = models.CharField(choices=UNI_DIV, max_length=50, blank=True)
    home_town = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    starred = models.ManyToManyField(Listing)

    # Check if the user has a verified uchicago email address
    def uchicago_email(self):
        email_list = EmailAddress.objects.filter(user=self.user, verified=True)
        for email in email_list:
            if '@uchicago.edu' in email.email:
                return True
        return False

    def social_account(self, account):
        if SocialAccount.objects.filter(user=self.user, provider=account):
            return True
        return False

    def get_listings(self):
        return Listing.objects.filter(user=self.user)

    def get_absolute_url(self):
        return reverse('public_profile', args=[str(self.id)])

    """ Checks whether the provided listing id is starred by user """
    def is_starred(self, listing_id):
        if (self.starred.filter(id=listing_id).exists()):
            return True
        return False

    def get_primary_email(self):
        return EmailAddress.objects.get(user=self.user, primary=True)

    def get_verifications(self):
        """Gets all verified/connected verifications and unconnected verifications"""
        v = [("Email Address", "Verified")]
        uv = []
        if (self.uchicago_email()):
            v.append(("UChicago Email", "Verified"))
        else:
            uv.append(("UChicago Email", "Not Verified"))

        if (self.social_account('facebook')):
            v.append(("Facebook", "Connected"))
        else:
            uv.append(("Facebook", "Not Connected"))

        if (self.social_account('google')):
            v.append(("Google", "Connected"))
        else:
            uv.append(("Google", "Not Connected"))

        if (self.social_account('linkedin')):
            v.append(("Linkedin", "Connected"))
        else:
            uv.append(("Linkedin", "Not Connected"))
        return (v, uv)


def user_post_save(sender, instance, created, **kwargs):
    # Create a user profile when a new user account is created
    if created:
        p = ExtendedUser()
        p.user = instance
        p.save()


post_save.connect(user_post_save, sender=User)
