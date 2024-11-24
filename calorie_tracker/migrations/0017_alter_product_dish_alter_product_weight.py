# Generated by Django 4.1.3 on 2023-03-27 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calorie_tracker', '0016_alter_day_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie_tracker.dish', verbose_name='Блюдо'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.IntegerField(verbose_name='Вес'),
        ),
    ]
