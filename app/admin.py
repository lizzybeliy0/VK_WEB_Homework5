from django.contrib import admin
from app import models

admin.site.register(models.Profile)
admin.site.register(models.Tag)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.QuestionVote)
admin.site.register(models.AnswerVote)
admin.site.register(models.QuestionTag)