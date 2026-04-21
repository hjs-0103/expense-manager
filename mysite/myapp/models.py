from django.db import models
from django.utils import timezone

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField()
    category = models.CharField()
    date = models.DateField(default=timezone.now)


    def __str__(self):
       return self.name