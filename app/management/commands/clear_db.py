from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Tag, Profile, User, Question, Answer, QuestionVote, AnswerVote, QuestionTag

class Command(BaseCommand):
    help = "Clear all data from the database"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Clearing database...")
            
            QuestionTag.objects.all().delete()
            self.stdout.write("Question tags deleted")
            
            AnswerVote.objects.all().delete()
            self.stdout.write("Answer votes deleted")
            
            QuestionVote.objects.all().delete()
            self.stdout.write("Question votes deleted")
            
            Answer.objects.all().delete()
            self.stdout.write("Answers deleted")
            
            Question.objects.all().delete()
            self.stdout.write("Questions deleted")
            
            Tag.objects.all().delete()
            self.stdout.write("Tags deleted")
            
            Profile.objects.all().delete()
            self.stdout.write("Profiles deleted")
            
            User.objects.all().delete()
            self.stdout.write("Users deleted")
            
            self.stdout.write(self.style.SUCCESS("Database cleared successfully!")) 