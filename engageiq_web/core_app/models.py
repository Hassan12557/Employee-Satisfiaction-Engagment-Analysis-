# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
#
#
# class SatisfactionPrediction(models.Model):
#     """
#     Database table to track every ML evaluation run by authenticated HR users.
#     """
#     # Links record to the specific logged-in HR account
#     hr_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
#
#     # Core input metrics from your Apple-inspired sliders (scaled 1 to 10)
#     compensation = models.FloatField()
#     career_progression = models.FloatField()
#     work_life_balance = models.FloatField()
#     manager_relationship = models.FloatField()
#
#     # The output calculated by your pre-trained Random Forest model
#     predicted_satisfaction = models.FloatField()
#
#     # Audit tracking metrics
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created_at']  # Keeps newest evaluations appearing first
#
#     def __str__(self):
#         return f"Prediction {self.predicted_satisfaction:.1f}/10 by {self.hr_manager.username} ({self.created_at.strftime('%Y-%m-%d')})"

from django.db import models
from django.contrib.auth.models import User
import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class ProfileOTP(models.Model):
    """
    Ties into the standard User model, tracking unique registration
    verification digits and operational activation states.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_valid(self):
        # The OTP expires exactly 5 minutes after creation
        return timezone.now() < self.created_at + datetime.timedelta(minutes=5)

    def generate_new_otp(self):
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.created_at = timezone.now()
        self.save()
        return self.otp_code
class SatisfactionPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    compensation = models.IntegerField()
    career_progression = models.IntegerField()
    work_life_balance = models.IntegerField()
    manager_relationship = models.IntegerField()
    predicted_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # FIXED: Changed from '__string__' to standard Django '__str__'
        return f"Prediction {self.predicted_score} - {self.created_at.date()}"
