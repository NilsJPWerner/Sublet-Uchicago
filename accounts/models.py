from django.db import models

#Disclaimer: Our models are based on https://github.com/sczizzo/Dhaka/blob/develop/db/schema.rb
# Create your models here.

class listing(models.Model):
	description = models.CharField(null=False, max_length=300)
	details = models.TextField(null=False, max_length=2000)
	price = models.IntegerField(default=0)
	status = models.IntegerField(default=0)
	# seller_id = models.OneToOneField(user) 
	created_at = models.DateTimeField(auto_now_add=True, null=False)
	updated_at = models.DateTimeField(auto_now=True, null=False)
	# permalink = models.CharField(blank=False, null=False, max_length=300)
	renewed_at = models.DateTimeField(default=None, null=True)
	renewals = models.IntegerField(default=0)
	published = models.BooleanField(default=True)
	location = models.CharField(null=True, max_length=200)



# class images(models.Model):
# 	listing_id = models.IntegerField(null=False) #Maybe implement as foreignkey?
# 	created_at = models.DateTimeField(auto_now_add=True, null=False)
# 	updated_at = models.DateTimeField(auto_now=True, auto_now_add=True, null=False)
# 	photo_file_name = models.CharField(max_length=150)
# 	photo_content_type = models.CharField(max_length=20)
# 	photo_file_size = models.IntegerField(null=False)

