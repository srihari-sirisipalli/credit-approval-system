# Generated by Django 5.0.1 on 2024-01-23 08:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_app', '0008_alter_customer_age_alter_customer_monthly_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='approved_limit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='monthly_salary',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
