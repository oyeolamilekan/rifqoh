from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
# Create your models here.
CONDITIONS = (

	(100, 'Extremely satisfied'),
	(70, 'Moderately satisfied'),
	(40, 'Slightly satisfied'),
	(10, 'Neutral'),
	(5, 'Slightly dissatisfied'),
	(2, 'Moderately dissatisfied'),
	(1, 'Exteremely dissatisfied'),
)

# Theme by the user collects user data does
# Magic with it
class UserTheme(models.Model):
	user = models.CharField(max_length=200,blank=True,null=True)
	theme = models.BooleanField(max_length=200,blank=False,default=True)
	timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def __str__(self):
		return '{} theme is {}'.format(user,theme)
	
	# For the admin magic that's it
	class Meta:
		ordering = ['-timestamp']
		verbose_name = 'User Theme'
		verbose_name_plural = 'User Theme'

# Products downloaded by the crawler
class Products(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True,related_name='who_did_it')
	name = models.CharField(max_length=300)
	price = models.CharField(max_length=300)
	real_price = models.IntegerField(default=0)
	image = models.ImageField(blank=True,null=True,max_length=355)
	source_url = models.CharField(max_length=300)
	shop = models.CharField(max_length=300)
	num_of_clicks = models.IntegerField(default=0)
	createdate = models.DateTimeField(auto_now_add=True)
	old_price = models.CharField(max_length=200,default='')
	old_price_digit = models.IntegerField(default=0)
	sub_genre = models.CharField(max_length=200,blank=True,null=True,default='')
	genre = models.CharField(max_length=200,blank=True,null=True,default='')
	subcriptions = models.ManyToManyField(settings.AUTH_USER_MODEL)

	# Returns the name of the product
	def __str__(self):
		return self.name

	# Again Does something's i don't undetstand
	class Meta:
		ordering = ['-id']
		verbose_name = 'Products'
		verbose_name_plural = 'Products'

# Calculates how many clicks for Trending page
class Analytics(models.Model):
	product = models.OneToOneField(Products) 
	number_of_clicks = models.IntegerField(default=0)
	createdate = models.DateTimeField(auto_now_add=True)

	# Returns the string attribute back to the admin
	def __str__(self):
		return '{} has {} clicks'.format(self.product, self.number_of_clicks)

	# Does things that i don't understand
	class Meta:
		ordering = ['-number_of_clicks']
		verbose_name = 'Analytics'
		verbose_name_plural = 'Analytics'

# Feedbacks from the user
class Feedback(models.Model):
	feelings = models.IntegerField(choices=CONDITIONS,blank=True,null=True)
	url_locator = models.CharField(blank=True,null=True,max_length=200)
	content = models.TextField(blank=True,null=True)
	createdate = models.DateTimeField(auto_now_add=True,blank=True,null=True)

	# Returns the string content for the admin stuff
	def __str__(self):
		return self.content

# Creates the analytics table automatically when a new product is being downloaded
def create_products(sender,**kwargs):
	if kwargs['created']:
		products = Analytics.objects.create(product=kwargs['instance'])

# Activates the function automatically.
post_save.connect(create_products, sender=Products)
