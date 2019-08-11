from django.urls import path, re_path
from .views import UserRegistration, UserLogin, AskAQuestion, Quora_feed, Answer_the_question


urlpatterns = [
	path('registration/', UserRegistration.as_view(), name = 'registration'),
	path('', UserLogin.as_view(), name = "login"),
	re_path(r'^question/(?P<user>[\w]+)/$', AskAQuestion.as_view(), name = 'question'),
	re_path(r'^feed/(?P<user>[\w]+)/$', Quora_feed.as_view(), name = 'quora_feed'),
	re_path(r'^feed/(?P<user>[\w]+)/(?P<question>[a-zA-Z0-9_? ]+)/$', Answer_the_question.as_view(), name = 'answer_field'),
]