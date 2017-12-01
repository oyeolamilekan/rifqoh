from django.db import models

# Create your models here.
SECTION_C = (('Technical','Technical'),('Tips','Tips'))

class Post(models.Model):
	topic = models.CharField(max_length=200)
	post = models.TextField(max_length=200)
	slug = models.SlugField(max_length=200)
	section = models.CharField(max_length=200,choices=SECTION_C)
	date_added = models.DateTimeField()

	def __str__(self):
		return self.topic