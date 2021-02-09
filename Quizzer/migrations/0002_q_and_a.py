# Generated by Django 3.1.4 on 2021-01-20 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quizzer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Q_And_A',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=256)),
                ('answear', models.CharField(max_length=256)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quizzer.quiz')),
            ],
        ),
    ]
