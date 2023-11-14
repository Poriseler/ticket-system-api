# Generated by Django 4.2.6 on 2023-11-03 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('LOW', 'Low'), ('MODERATE', 'Moderate'), ('URGENT', 'Urgent')], default='LOW', max_length=255),
        ),
    ]