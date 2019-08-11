from django.shortcuts import render
from .forms import userregistration, userlogin, AskQuestion, Answer_form
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import View
from .models import user, Question, Answer

class UserRegistration(View):
	def get(self, request):
		template_name = 'registration.html'
		form = userregistration()
		content = {'form' : form}
		return render(request, template_name, content)

	def post(self, request):
		template_name = 'registration.html'
		form = userregistration(request.POST)
		q_len = len(user.objects.filter(username = request.POST['username']))
		if form.is_valid() and not q_len:
			form.save()
			return HttpResponseRedirect(reverse('login'))

		content = {'form' : userregistration(), 'form_error' : form.errors}	
		return render(request, template_name, content)


class UserLogin(View):
	def get(self, request):
		template_name = 'login.html'
		form = userlogin()
		content = {'form' : form}
		return render(request, template_name, content)

	def post(self, request):
		template_name = 'login.html'
		name = request.POST.get('username')
		password1 = request.POST.get('password')
		is_authenticated = authenticate(username = name, password = password1)
		if is_authenticated :
			return HttpResponseRedirect(reverse('quora_feed', kwargs = {'user' : name})) 
			'''logged_in_user = user.objects.get(username = name)
			questions = Question.objects.all()
			answers = Answer.objects.all()
			ques_ans = {} #creating a dictionary to hold the question and list of answers as key-value pairs
			for answer in answers : 
				if answer.question.question not in ques_ans.keys():
					ques_ans[answer.question.question] = []
				ques_ans[answer.question.question].append(answer)
					

			context = {
			'logged_in_user' : logged_in_user,
			'ques_ans' : ques_ans,
			}
			return render(request, "feed.html", context)
		
		correct = False
		content = {
		'form' : userlogin(), 
		'login_error' : "Enter the correct username or password",
		'exist' : correct,
		}
		return render(request, template_name, content)
		try:
			check_name = user.objects.get(username = name)	
		except user.DoesNotExist as e:
			raise e
			content = {
			'form' : userlogin(), 
			'login_error' : "Enter the correct username or password",
			}
			return render(request, template_name, content)
		correct = True
		if check_name.password != password:
			correct = False
			content = {
			'form' : userlogin(), 
			'login_error' : "Enter the correct username or password",
			'exist' : correct,
			}'''
			

		
def authenticate(username = None, password = None):
	if username and password:
		user1 = user.objects.filter(username = username)
		if len(user1) == 1:
			if password == user1.first().password:
				return True
			else:
				return False

	return False
	
class AskAQuestion(View):
	def get(self, request, *args, **kwargs):
		asked_user = user.objects.get(username = kwargs['user'])
		form = AskQuestion()
		content = {'form' : form, 'user' : asked_user}
		return render(request, 'question.html', content)

	def post(self, request, *args, **kwargs):
		form = AskQuestion(request.POST)
		if form.is_valid() and user.objects.filter(username = request.POST['asked_user']).exists():
			Question.objects.create(
				question = request.POST['question'],
				asked_user = user.objects.get(username = request.POST['asked_user']),
				)
			return HttpResponseRedirect(reverse('quora_feed', kwargs = {'user' : request.POST['asked_user']}))


class Quora_feed(View):#search for Q!!!
	def get(self, request, *args, **kwargs):
		current_user = user.objects.get(username = kwargs['user'])
		questions = Question.search_question.all()
		answers = Answer.objects.all()
		q_query = request.GET.get('query')
		if q_query:
			questions = questions.search(q_query)

		ques_ans = {} #creating a dictionary to hold the question and list of answers as key-value pairs
		for q in questions:
			ques_ans[q.question] = []
			for a in answers:
				if a.question.question == q.question:
					ques_ans[q.question].append(a)

		context = {
			'logged_in_user' : current_user,
			'ques_ans' : ques_ans,
			}
		return render(request, 'feed.html', context)



class Answer_the_question(View):
	def get(self, request, *args, **kwargs):
		asked_question = kwargs['question']
		answering_user = kwargs['user']
		print(asked_question)
		context = {
		'asked_question' : asked_question,
		'answering_user' : answering_user,
		'form' : Answer_form()
		}
		return render(request, "answer.html", context)

	def post(self, request, *args, **kwargs):
		print(request.POST)
		form = Answer_form(request.POST)
		if form.is_valid() :
			Answer.objects.create(
				answer = request.POST['answer'],
				question = Question.objects.get(question = kwargs['question']),
				answered_user = user.objects.get(username = kwargs['user']),
				)
			return HttpResponseRedirect(reverse('quora_feed', kwargs = {'user' : kwargs['user']}))
 


