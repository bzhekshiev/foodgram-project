# Generated by Django 3.1 on 2020-12-29 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20201228_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='class_name',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='slug',
        ),
    ]