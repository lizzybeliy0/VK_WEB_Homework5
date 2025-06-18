from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Question, Tag, Answer, QuestionVote, AnswerVote, Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)

def index(request):
    questions = Question.objects.latest()
    return render(request, 'index.html', {
        'page_obj': paginate(questions, request),
        'tab': 'new'
    })

def hot(request):
    questions = Question.objects.popular()
    return render(request, 'hot.html', {
        'page_obj': paginate(questions, request),
        'tab': 'hot'
    })

def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.for_question(question_id)
    return render(request, 'question.html', {
        'question': question,
        'page_obj': paginate(answers, request)
    })

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = tag.questions.all()
    return render(request, 'tag.html', {
        'page_obj': paginate(questions, request),
        'tab': 'tag',
        'tag': tag
    })

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

def logout(request):
    auth_logout(request)
    return redirect(reverse('index') + "?after=logout")

