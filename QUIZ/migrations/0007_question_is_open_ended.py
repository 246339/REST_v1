# Generated by Django 5.0.7 on 2024-07-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QUIZ', '0006_alter_question_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_open_ended',
            field=models.BooleanField(default=False),
        ),
    ]