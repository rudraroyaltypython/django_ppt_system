# presenter/models.py
from django.db import models


class Presentation(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    def slide_count(self):
        return self.slides.count()   # thanks to related_name


class Slide(models.Model):
    presentation = models.ForeignKey(
        Presentation,
        on_delete=models.CASCADE,
        related_name="slides"   # 👈 important for cleaner access
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    code_snippet = models.TextField(blank=True, null=True)
    slide_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["slide_order"]

    def __str__(self):
        return f"{self.title} ({self.presentation.topic})"


# ---------- new models for gamification ----------
class Participant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Score(models.Model):
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, related_name="scores"
    )
    presentation = models.ForeignKey(
        Presentation, on_delete=models.CASCADE, null=True, blank=True, related_name="scores"
    )
    points = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant} — {self.points} pts"
