from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


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
    description = models.TextField(blank=True)


def user_post_save(sender, instance, created, **kwargs):
    # Create a user profile when a new user account is created
    if created:
        p = ExtendedUser()
        p.user = instance
        p.save()
