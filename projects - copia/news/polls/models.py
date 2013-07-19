from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

NEWS_RATING_CHOICES = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
)

NEWS_CATEGORY_CHOICES = (
    ('Fortaleza', 'Fortaleza'),
    ('Oportunidad', 'Oportunidad'),
    ('Debilidad', 'Debilidad'),
    ('Amenaza', 'Amenaza'),
)



from django.db import models

# Create your models here.
class Person (models.Model):
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	job_description = models.CharField(max_length=100)

	def __unicode__(self):
		return self.first_name + str(' ') + self.last_name

	#def create_person_user_callback(sender, instance, **kwargs):
	#	person, new = Person.objects.get_or_create(user=instance)
	#	post_save.connect(create_person_user_callback, User)

class News (models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	date = models.DateTimeField('date published')
	source = models.CharField(max_length=300)
	category = models.CharField(max_length=100, choices=NEWS_CATEGORY_CHOICES)
	rating = models.IntegerField(max_length=3, choices=NEWS_RATING_CHOICES, default=0)
	#comments = models.ManyToManyField(Comment, blank=True)
	user = models.ForeignKey(Person)

	def __unicode__(self):
		return self.title #+ str(self.id) # self.title

class Comment (models.Model):
	description = models.CharField(max_length=400)
	date = models.DateTimeField('date published')
	user = models.ForeignKey(Person)
	news_item = models.ForeignKey(News)
	def __unicode__(self):
		return str(self.user) + str(': ') + str(self.description)
