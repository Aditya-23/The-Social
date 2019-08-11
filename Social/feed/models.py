from django.db import models
from django.db.models import Q

# Create your models here.

class Question_query(models.query.QuerySet):
	def search(self, query = None):
		return self.filter(
			Q(question__icontains = query)
			)

class Search(models.Manager):
	def get_queryset(self, query = None):
		return Question_query(self.model, using = self._db)

	def search(self, query = None):
		return self.get_queryset().search(query)

class user(models.Model):
	username = models.CharField(max_length = 20, blank = False)
	password = models.CharField(max_length = 20, blank = False)
	firstname = models.CharField(max_length = 40, blank = False)
	lastname = models.CharField(max_length = 40, blank = False)
	email = models.EmailField(max_length = 40, blank = False)

	#search_user = Search()

	def __str__(self):
		return self.username


class Question(models.Model):
	question = models.CharField(max_length = 100, blank = False)
	asked_user = models.ForeignKey('user', on_delete = models.CASCADE)
	datetime = models.DateTimeField(auto_now = True)

	objects = models.Manager()
	search_question = Search()

	def __str__(self):
		return self.question
		

class Answer(models.Model):
	answer = models.CharField(max_length = 1000, blank = False)
	datetime = models.DateTimeField(auto_now = True)
	question = models.ForeignKey('Question', on_delete = models.CASCADE)
	answered_user = models.ForeignKey('user', on_delete = models.CASCADE)

	def __str__(self):
		return self.answer