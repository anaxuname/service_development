# Generated by Django 4.2.7 on 2024-02-05 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image_preview',
            field=models.ImageField(blank=True, null=True, upload_to='material/', verbose_name='изображение'),
        ),
    ]