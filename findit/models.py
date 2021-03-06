from django.conf import settings
from django.db import models
from django.db.models.signals import post_save,pre_save
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from watson import search as watson

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
# Oyeolamilekan1

# Theme by the user collects user data does
# Magic with it


class ProductList(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class UserTheme(models.Model):
    user = models.CharField(max_length=200, blank=True, null=True)
    theme = models.BooleanField(max_length=200, blank=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{} theme is {}'.format(self.user, self.theme)

    # For the admin magic that's it
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'User Theme'
        verbose_name_plural = 'User Theme'


# Products downloaded by the crawler
class Products(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='who_did_it',on_delete=True)
    name = models.CharField(max_length=300)
    price = models.CharField(max_length=300)
    converted_price = models.CharField(max_length=300, blank=True, null=True)
    real_price = models.IntegerField(default=0)
    objects = ProductList()
    real_price_2 = models.IntegerField(default=0)
    image = models.ImageField(max_length=355)
    source_url = models.CharField(max_length=700)
    shop = models.CharField(max_length=300)
    country_code = models.CharField(max_length=200,blank=True,null=True)
    num_of_clicks = models.IntegerField(default=0)
    createdate = models.DateTimeField(auto_now_add=True)
    old_price = models.CharField(max_length=200, blank=True, null=True)
    old_price_2 = models.CharField(max_length=200, blank=True, null=True)
    old_price_digit = models.IntegerField(default=0)
    old_price_digit_2 = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True, null=True)
    sub_genre = models.CharField(max_length=200, blank=True, null=True, default='')
    genre = models.CharField(max_length=200, blank=True, null=True, default='')
    subcriptions = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,)
    lppo = models.CharField(max_length=200, blank=True, null=True)

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
    product = models.OneToOneField(Products,on_delete=models.CASCADE)
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

# Handles the Tips database
class Tips(models.Model):
    body = models.TextField()
    image = models.ImageField(blank=True, null=True)
    image_1 = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['-id']
        verbose_name = 'Tip'
        verbose_name_plural = 'Tips'


# Feedbacks from the user
class Feedback(models.Model):
    feelings = models.IntegerField(blank=True, null=True)
    current_location = models.CharField(max_length=200, null=True, blank=True)
    url_locator = models.CharField(blank=True, null=True, max_length=200)
    email = models.EmailField(max_length=200, default='')
    content = models.TextField(blank=True, null=True)
    createdate = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # Returns the string content for the admin stuff
    def __str__(self):
        return self.content

def create_slug(instance, new_slug=None):
    slug = slugify('%s-%s-%s' % (instance.name[:10],instance.shop,get_random_string(length=4)))
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Products)


# Creates the analytics table automatically when a new product is being downloaded
def create_products(sender, **kwargs):
    if kwargs['created']:
        products = Analytics.objects.create(product=kwargs['instance'])


# Activates the function automatically.
post_save.connect(create_products, sender=Products)

watson.register(Products)