# Generated by Django 4.0.4 on 2022-06-14 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_pizzas_min_price_alter_pizzas_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cookie_name', models.CharField(max_length=1000)),
            ],
        ),
    ]
