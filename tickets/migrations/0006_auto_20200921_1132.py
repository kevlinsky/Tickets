# Generated by Django 3.1.1 on 2020-09-21 11:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=1000000, primary_key=True, serialize=False),
        ),
    ]
