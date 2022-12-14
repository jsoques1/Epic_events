# Generated by Django 4.1 on 2022-08-30 15:18

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
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('payment_due', models.DateField()),
                ('is_signed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('is_completed', models.BooleanField(default=False)),
                ('attendees', models.PositiveIntegerField()),
                ('event_date', models.DateTimeField()),
                ('notes', models.TextField(blank=True, max_length=800, null=True)),
                ('contract', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.contract')),
                ('support', models.ForeignKey(limit_choices_to={'role': 'SUPPORT'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=50)),
                ('company_name', models.CharField(max_length=70)),
                ('phone_number', models.CharField(max_length=20)),
                ('mobile_number', models.CharField(max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('is_signed', models.BooleanField(default=False)),
                ('salesman', models.ForeignKey(limit_choices_to={'role': 'SALES'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.customer'),
        ),
        migrations.AddField(
            model_name='contract',
            name='salesman',
            field=models.ForeignKey(limit_choices_to={'role': 'SALES'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
