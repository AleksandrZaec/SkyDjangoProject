# Generated by Django 4.2 on 2024-05-08 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False, verbose_name='Верификация почты'),
        ),
        migrations.AddField(
            model_name='user',
            name='ver_code',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='проверочный код'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активность'),
        ),
    ]
