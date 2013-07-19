from django.contrib import admin
from polls.models import Person, Comment, News

admin.site.register(Person)
admin.site.register(Comment)
admin.site.register(News)
