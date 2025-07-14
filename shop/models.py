from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='без описания')

    def __str__(self):
        return self.name
    

class Course(models.Model):
    title = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    published = models.DateTimeField()
    category = models.ForeignKey(to=Category, related_name='courses', on_delete=models.CASCADE)

    class Meta:
        db_table = 'catalog_course'
        ordering = ['-published']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('course_detail', args=[self.pk])
    
    def is_recent(self):
        return self.published >= timezone.now() - timedelta(days=7)


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    

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
    
