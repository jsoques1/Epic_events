# Generated by Django 4.1 on 2022-08-11 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crmuser',
            name='role',
            field=models.CharField(default='IT', max_length=7, verbose_name=[('IT', 'IT'), ('SALES', 'SALES'), ('SUPPORT', 'SUPPORT')]),
        ),
    ]
