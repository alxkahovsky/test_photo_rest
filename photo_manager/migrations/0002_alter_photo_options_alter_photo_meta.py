# Generated by Django 4.1.5 on 2023-01-17 13:44

from django.db import migrations, models
import photo_manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'verbose_name': 'Фото', 'verbose_name_plural': 'Фото'},
        ),
        migrations.AlterField(
            model_name='photo',
            name='meta',
            field=models.JSONField(blank=True, default=photo_manager.models.defult_meta, null=True, verbose_name='Метаданные'),
        ),
    ]
