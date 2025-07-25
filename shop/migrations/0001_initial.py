# Generated by Django 5.2.3 on 2025-06-30 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('available', models.BooleanField(default=True, verbose_name='наличие')),
                ('data_added', models.DateField(auto_now_add=True, verbose_name='дата добавления')),
                ('categories', models.ManyToManyField(related_name='products', to='shop.category')),
            ],
        ),
    ]
