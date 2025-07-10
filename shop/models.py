from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=30, verbose_name='название')
    description = models.TextField(verbose_name='описание', blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2, verbose_name='цена')
    available = models.BooleanField(verbose_name='наличие', default=True)
    data_added = models.DateField(auto_now_add=True, verbose_name='дата добавления')
    categories = models.ManyToManyField('Category', related_name='products')
    
class Icecream(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(verbose_name='наличии', default=True)

    def __str__(self):
        return self.name