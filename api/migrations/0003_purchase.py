# Generated by Django 3.1 on 2021-01-03 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20201231_2056'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_subscribe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_purchase', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_purchase', to='recipes.recipe', verbose_name='рецепт')),
            ],
            options={
                'verbose_name': 'список покупок',
                'verbose_name_plural': 'списки покупок',
                'unique_together': {('author', 'recipe')},
            },
        ),
    ]