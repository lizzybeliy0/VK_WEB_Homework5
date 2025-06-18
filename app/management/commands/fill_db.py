from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from random import choice, choices, randint
from time import time
from app.models import *

def printProgress(self, progress, max_value, start_time, message):
    if progress != -1:
        self.stdout.write(
            self.style.HTTP_INFO(f'{message.ljust(25, " ")} [{format(time() - start_time, "2.2f")}s; {int(progress / max_value * 100)}%]    \r'),
            ending=""
        )
        self.stdout.flush()
    else:
        self.stdout.write(
            self.style.SUCCESS(f'{message.ljust(25, " ")} [{format(time() - start_time, "2.2f")}s] - Done!'),
        )

class Command(BaseCommand):
    help = "Command for generate test database"

    def add_arguments(self, parser):
        parser.add_argument("ratio", nargs="+", type=int)

    def handle(self, *args, **options):
        ratio = options["ratio"][0]
        dbBuffer = 1000

        with transaction.atomic():
            # Создание тэгов
            index = 0
            totalCount = ratio
            allTags = [None] * totalCount

            start = time()
            printProgress(self, 0, totalCount, start, "Создание тэгов...")
            while index < totalCount:
                newTags = []
                for j in range(min(totalCount - index, dbBuffer)):
                    newTag = Tag(name=f"tag {index}")
                    newTags.append(newTag)
                    allTags[index] = newTag
                    index += 1
                    printProgress(self, index, totalCount, start, "Создание тэгов...")
                Tag.objects.bulk_create(newTags)
            printProgress(self, -1, totalCount, start, "Создание тэгов...")

            #профили и пользователи
            index = 0
            totalCount = ratio
            allProfiles = [None] * totalCount

            start = time()
            printProgress(self, 0, totalCount, start, "Создание пользователей...")
            while index < totalCount:
                newProfiles = []
                newUsers = []
                for j in range(min(totalCount - index, dbBuffer)):
                    user = User(username=f"user_{index}", email=f"user_{index}@gmail.com", password="1234password1234")
                    profile = Profile(user=user, avatar="avatars/default.jpg")
                    allProfiles[index] = profile
                    newUsers.append(user)
                    newProfiles.append(profile)
                    index += 1
                    printProgress(self, index, totalCount, start, "Создание пользователей...")
                User.objects.bulk_create(newUsers)
                Profile.objects.bulk_create(newProfiles)
            printProgress(self, -1, totalCount, start, "Создание пользователей...")

            #вопросы
            index = 0
            totalCount = ratio * 10
            allQuestions = [None] * totalCount

            start = time()
            printProgress(self, 0, totalCount, start, "Создание вопросов...")
            while index < totalCount:
                newQuestions = []
                for j in range(min(totalCount - index, dbBuffer)):
                    author = choice(allProfiles)
                    question = Question(
                        title=f"Question {index + 1}",
                        content=f"This is question {index + 1}",
                        created_at=timezone.now(),
                        author=author,
                    )
                    allQuestions[index] = question
                    newQuestions.append(question)
                    index += 1
                    printProgress(self, index, totalCount, start, "Создание вопросов...")
                Question.objects.bulk_create(newQuestions)
            printProgress(self, -1, totalCount, start, "Создание вопросов...")

            #лайки для вопросов
            index = 0
            totalCount = ratio * 100
            allQuestionsLikes = set()

            start = time()
            printProgress(self, 0, totalCount, start, "Лайки для вопросов...")
            while index < totalCount:
                newLikes = []
                for j in range(min(totalCount - index, dbBuffer)):
                    author = choice(allProfiles)
                    question = choice(allQuestions)
                    pair = f"{author.id};{question.id}"
                    
                    if pair in allQuestionsLikes:
                        continue
                    
                    allQuestionsLikes.add(pair)
                    like = QuestionVote(
                        question=question,
                        voter=author,
                        value=choice([-1, 1])
                    )
                    newLikes.append(like)
                    index += 1
                    printProgress(self, index, totalCount, start, "Лайки для вопросов...")
                QuestionVote.objects.bulk_create(newLikes)
            printProgress(self, -1, totalCount, start, "Лайки для вопросов...")

            #тэги к вопросам
            index = 0
            totalCount = len(allQuestions)
            allQuestionTags = set()

            start = time()
            printProgress(self, 0, totalCount, start, "Тэги для вопросов...")
            while index < totalCount:
                newQuestionTags = []
                for j in range(min(totalCount - index, dbBuffer)):
                    question = allQuestions[index]
                    num_tags = randint(1, 2) 
                    tags = choices(allTags, k=num_tags)
                    
                    for tag in tags:
                        pair = f"{question.id};{tag.id}"
                        if pair not in allQuestionTags:
                            allQuestionTags.add(pair)
                            questionTag = QuestionTag(
                                question=question,
                                tag=tag,
                            )
                            newQuestionTags.append(questionTag)
                    
                    index += 1
                    printProgress(self, index, totalCount, start, "Тэги для вопросов...")
                
                if newQuestionTags:
                    QuestionTag.objects.bulk_create(newQuestionTags)
            printProgress(self, -1, totalCount, start, "Тэги для вопросов...")

            #ответы
            index = 0
            totalCount = ratio * 100
            allAnswers = [None] * totalCount

            start = time()
            printProgress(self, 0, totalCount, start, "Создание ответов...")
            while index < totalCount:
                newAnswers = []
                for j in range(min(totalCount - index, dbBuffer)):
                    author = choice(allProfiles)
                    question = choice(allQuestions)
                    answer = Answer(
                        question=question,
                        content=f"This is answer {index + 1}",
                        created_at=timezone.now(),
                        author=author,
                    )
                    allAnswers[index] = answer
                    newAnswers.append(answer)
                    index += 1
                    printProgress(self, index, totalCount, start, "Создание ответов...")
                Answer.objects.bulk_create(newAnswers)
            printProgress(self, -1, totalCount, start, "Создание ответов...")

            #лайки для ответов
            index = 0
            totalCount = ratio * 100
            allAnswersLikes = set()

            start = time()
            printProgress(self, 0, totalCount, start, "Лайки для ответов...")
            while index < totalCount:
                newLikes = []
                for j in range(min(totalCount - index, dbBuffer)):
                    author = choice(allProfiles)
                    answer = choice(allAnswers)
                    pair = f"{author.id};{answer.id}"
                    
                    if pair in allAnswersLikes:
                        continue
                    
                    allAnswersLikes.add(pair)
                    like = AnswerVote(
                        answer=answer,
                        voter=author,
                        value=choice([-1, 1])
                    )
                    newLikes.append(like)
                    index += 1
                    printProgress(self, index, totalCount, start, "Лайки для ответов...")
                AnswerVote.objects.bulk_create(newLikes)
            printProgress(self, -1, totalCount, start, "Лайки для ответов...")
        
        self.stdout.write(
            self.style.SUCCESS('-' * 42 + "\n" + "БД успешно сгенерирована!" + "\n" + '-' * 42),
        )