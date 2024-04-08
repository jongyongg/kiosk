from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, default=None)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True) # price 필드 추가

    def __str__(self):
        return self.choice_text

class Order(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, default=None)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total_price 필드 추가

    def save(self, *args, **kwargs):
        # Calculate total price based on quantity and price
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)  # Call the superclass's save method to save the instance

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.name
class Menu(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name