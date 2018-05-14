from django.db import models
from django.contrib.auth.models import User

class Maruda(models.Model):
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = 'images/')
    icon = models.ImageField(upload_to = 'images/')
    text = models.TextField()
    url = models.TextField()

    votes_total = models.IntegerField(default = 1)

    date = models.DateTimeField()

    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def summary(self):
        return self.text[:100] + "..."

    def date_better(self):
        return self.date.strftime('%b %e %Y')

    def __str__(self):
        return self.title

class MarudaVoting(models.Model):
    maruda = models.ForeignKey(Maruda, on_delete=models.CASCADE, related_name='voted')
    voting = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voted_by')

    def __str__(self):
        return self.maruda.title + " by " + self.voting.username
