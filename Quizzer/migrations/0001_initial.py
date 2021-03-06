# Generated by Django 3.1.4 on 2021-05-05 21:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('question', models.CharField(max_length=256)),
                ('answer', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Quiz Name')),
                ('visible_to', models.CharField(choices=[('pub', 'Public'), ('pri', 'Private'), ('fri', 'Friends')], default='pub', max_length=3, verbose_name='Visible To')),
                ('modified_by', models.CharField(choices=[('pub', 'Public'), ('pri', 'Private'), ('fri', 'Friends')], default='pub', max_length=3, verbose_name='Modified By')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuizTtl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('range_max', models.IntegerField(default=0)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.profile')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.quiz')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(default='seq', max_length=6)),
                ('complete', models.BooleanField(default=False)),
                ('current_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.qa')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.profile')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.quiz')),
                ('quiz_total_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.quizttl')),
            ],
            options={
                'get_latest_by': 'date',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='qa',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.quiz'),
        ),
        migrations.CreateModel(
            name='AnswerTtl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0)),
                ('rangeMin', models.IntegerField(default=0)),
                ('rangeMax', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.qa')),
                ('quiz_total_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.quizttl')),
            ],
            options={
                'ordering': ['-weight'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnswerResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.qa')),
                ('quiz_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.quizresult')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
