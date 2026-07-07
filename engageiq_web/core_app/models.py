# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class SatisfactionPrediction(models.Model):
    """
    Database table to track every ML evaluation run by authenticated HR users.
    """
    # Links record to the specific logged-in HR account
    hr_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')

    # Core input metrics from your Apple-inspired sliders (scaled 1 to 10)
    compensation = models.FloatField()
    career_progression = models.FloatField()
    work_life_balance = models.FloatField()
    manager_relationship = models.FloatField()

    # The output calculated by your pre-trained Random Forest model
    predicted_satisfaction = models.FloatField()

    # Audit tracking metrics
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Keeps newest evaluations appearing first

    def __str__(self):
        return f"Prediction {self.predicted_satisfaction:.1f}/10 by {self.hr_manager.username} ({self.created_at.strftime('%Y-%m-%d')})"