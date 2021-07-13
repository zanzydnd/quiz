# Generated by Django 2.2.24 on 2021-07-13 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('type', models.CharField(choices=[('TEXT', 'TEXT'), ('SINGLE', 'SINGLE'), ('MULTIPLE', 'MULTIPLE')], default='TEXT', max_length=15)),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_right', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Question')),
            ],
            options={
                'verbose_name': 'Ответ для вопроса',
                'verbose_name_plural': 'Ответы для вопросов',
                'db_table': 'question_answer',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('chosen_answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.QuestionAnswer')),
                ('text_question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ответ пользователя',
                'verbose_name_plural': 'Ответы пользователей',
                'db_table': 'user_answer',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(auto_now=True)),
                ('end_date', models.DateTimeField()),
                ('description', models.TextField()),
                ('questions', models.ManyToManyField(related_name='quiz', to='api.Question')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
                'db_table': 'quiz',
            },
        ),
    ]