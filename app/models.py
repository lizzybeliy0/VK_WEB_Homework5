from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Coalesce


class ProfileManager(models.Manager):
    def popular(self):
        return self.annotate(
            answers_count=models.Count("answers")
        ).order_by("-answers_count")[:5]

class TagManager(models.Manager):
    def popular(self):
        return self.annotate(
            question_count=models.Count("questions")
        ).order_by("-question_count")[:15]

class QuestionManager(models.Manager):
    def latest(self):
        return self.order_by("-created_at")
    
    def popular(self):
        return self.annotate(
            rating=Coalesce(models.Sum('votes__value'), 0)
        ).order_by("-rating", "-created_at")
    

class AnswerManager(models.Manager):
    def for_question(self, question_id):
        return self.filter(question_id=question_id).annotate(
            likes_count=models.Count("votes", filter=models.Q(votes__value=1))
        ).order_by("-is_accepted", "-likes_count", "created_at")
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/', default='images/default.jpg')
    objects = ProfileManager()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    objects = TagManager()

class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, through='QuestionTag', related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = QuestionManager()

    def changeRightAnswer(self, right_answer):
        self.answers.update(is_accepted=False)
        right_answer.is_accepted = True
        right_answer.save()
    
    def has_like(self, user):
        if not user.is_authenticated:
            return False
        return self.votes.filter(voter__user=user).exists()

    def get_rating(self):
        return self.votes.aggregate(total=models.Sum('value'))['total'] or 0


class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = AnswerManager()
    
    def has_like(self, user):
        if not user.is_authenticated:
            return False
        return self.votes.filter(voter__user=user).exists()

    def get_rating(self):
        return self.votes.aggregate(total=models.Sum('value'))['total'] or 0


class QuestionVote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])
    
    class Meta:
        unique_together = ('question', 'voter')

class AnswerVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])
    
    class Meta:
        unique_together = ('answer', 'voter')

class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('question', 'tag')