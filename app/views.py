from django.shortcuts import render
from django.shortcuts import HttpResponse
import copy
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'title' : f'Title {i}',
        'id' : i,
        'text' : f'This is text for q = {i}',
        #'img_path': f"img/[i].img"
        'img_path': '/img/sunn.jpg',
        'tags': ['first', 'second'] if i % 2 == 0 else ['third', 'fourth']
    } for i in range(30)
]

ANSWERS = [
    {
        'title' : f'Title {i}',
        'id' : i,
        'text' : f'This is text for a = {i}',
        #'img_path': f"img/[i].img"
        'img_path': '/img/cosmos.jpg'
    } for i in range(15)
]

TAGS = ['first', 'second', 'third', 'fourth', 'fivth']


def index (request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render (request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def hot (request):
    q = list(reversed(copy.deepcopy(QUESTIONS)))
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(q, 5)
    page = paginator.page(page_num)
    return render (request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})

def question(request, question_id):
    
    #return render (request, 'question.html', context={'question': QUESTIONS[question_id]})
    question = QUESTIONS[question_id]
    
    answers_list = ANSWERS
    
    page_num = request.GET.get('page', 1)
    paginator = Paginator(answers_list, 5)
    page_obj = paginator.get_page(page_num)
    
    return render(request, 'question.html', {
        'question': question,
        'answers': page_obj.object_list,
        'page_obj': page_obj
    })

def tag(request, tag_name):
    filtered_questions = [q for q in QUESTIONS if tag_name in q.get('tags', [])]
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(filtered_questions, 5)
    page = paginator.page(page_num)
    return render(request, 'tag.html', {
        'questions': page.object_list,
        'page_obj': page,
        'tag_name': tag_name
    })

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')