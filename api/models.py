from django.db import models


class Pizzas(models.Model):
    id = models.IntegerField(primary_key=True)
    pizza = models.JSONField()
    min_price = models.IntegerField()


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    cookie_name = models.CharField(max_length=1000)


class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.CharField(max_length=100)