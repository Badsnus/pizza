# Generated by Django 4.0.4 on 2022-06-11 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizzas',
            name='category',
        ),
        migrations.RemoveField(
            model_name='pizzas',
            name='imageUrl',
        ),
        migrations.RemoveField(
            model_name='pizzas',
            name='name',
        ),
        migrations.RemoveField(
            model_name='pizzas',
            name='price',
        ),
        migrations.RemoveField(
            model_name='pizzas',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='pizzas',
            name='sizes',
        ),
        migrations.RemoveField(
            model_name='pizzas',
            name='types',
        ),
        migrations.AddField(
            model_name='pizzas',
            name='pizza',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
    ]