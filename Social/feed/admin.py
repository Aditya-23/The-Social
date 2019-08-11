from django.contrib import admin
from .models import user, Question, Answer
# Register your models here.
admin.site.register(user)
admin.site.register(Question)
admin.site.register(Answer)