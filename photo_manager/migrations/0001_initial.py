# Generated by Django 4.1.5 on 2023-01-17 10:55

from django.db import migrations, models
import django.utils.timezone
import photo_manager.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='photos', verbose_name='Фотография')),
                ('meta', models.JSONField(default=photo_manager.models.defult_meta, verbose_name='Метаданные')),
                ('available', models.BooleanField(default=True, verbose_name='Доступно?')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата создания записи')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата ред-ия записи')),
            ],
        ),
    ]
