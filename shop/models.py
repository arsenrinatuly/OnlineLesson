from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.conf import settings

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
    


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Product2(models.Model):
    name = models.CharField(max_length=100)
class Order(models.Model):
    date = models.DateField()
    products = models.ManyToManyField(Product2, through='OrderItem')
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product2, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Actors(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)


class Movie(models.Model):
    name = models.CharField(max_length=50)
    year_created = models.DateField()
    actors = models.ManyToManyField(to=Actors, through='Cast')

class Cast(models.Model):
    actors = models.ForeignKey(Actors, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)


class BaseComment(models.Model):
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    class Meta:
        abstract = True

class UserComment(BaseComment):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)

class ModeratedComment(UserComment):
    is_approved = models.BooleanField(default=False)
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderated_commnts'
    )


class Comment(models.Model):
    text = models.TextField(blank=True, null=True)

    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='айдишник')

    content_object = GenericForeignKey('content_type','object_id')