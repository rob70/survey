from django.contrib import admin

# Register your models here.

from .models import Question, Topic

admin.site.register(Question)
admin.site.register(Topic)