# Generated by Django 4.2.7 on 2024-01-28 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogNewsLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_newsletter', models.DateTimeField(auto_now_add=True, verbose_name='Data Time Last Try')),
                ('status_mailing', models.IntegerField(choices=[(1, 'CREATED'), (2, 'PROCESSING'), (3, 'COMPLETED'), (4, 'ERROR')], default=1, verbose_name='Status')),
                ('answer_server', models.TextField(verbose_name='Answer from Server')),
            ],
        ),
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name NewsLetter')),
                ('time_mailing', models.TimeField(verbose_name='Time NewsLetter')),
                ('periodicity_mailing', models.CharField(max_length=50, verbose_name='Periodicity')),
                ('status_mailing', models.IntegerField(choices=[(1, 'CREATED'), (2, 'PROCESSING'), (3, 'COMPLETED'), (4, 'ERROR')], default=1, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Content')),
                ('newsletter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.newsletter')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('newsletter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.newsletter')),
            ],
        ),
    ]
