from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.enums import EventChoices, GenderChoices
# Create your models here.
    
class User(AbstractUser):

    full_name = models.CharField(max_length=100)
    email= models.EmailField(unique=True,)
    mobile_number = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=100, choices=GenderChoices.choices)
    username = models.CharField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'

    
    REQUIRED_FIELDS = ['full_name', 'mobile_number', 'dob', 'gender', 'username']


class SubmissionID(models.Model):

    submission_id = models.CharField(max_length=20,unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_submission_id")

class WebhookResponse(models.Model):
    submission_id = models.CharField(max_length=100)
    event_code = models.CharField(max_length=100,choices= EventChoices.choices)
    event_name = models.CharField(max_length=100)
    time_stamp = models.CharField(max_length=100)
    data = models.JSONField()
    
    # def get_user(self):
    #     """Get the user associated with this webhook response through the submission_id."""
    #     try:
    #         submission = SubmissionID.objects.get(submission_id=self.submission_id)
    #         return submission.user
    #     except SubmissionID.DoesNotExist:
    #         return None