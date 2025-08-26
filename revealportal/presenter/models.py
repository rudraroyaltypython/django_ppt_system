from django.db import models

class Presentation(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

class Slide(models.Model):
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    code_snippet = models.TextField(blank=True, null=True)
    slide_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
