# Generated by Django 4.1.3 on 2022-11-14 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calorie_tracker', '0015_alter_day_total_calories_alter_meal_total_calories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['id'], 'verbose_name': 'День', 'verbose_name_plural': 'Дни'},
        ),
    ]
