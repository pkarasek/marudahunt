# Generated by Django 2.0.2 on 2018-05-11 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marudy', '0005_maruda_hunter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maruda',
            name='hunter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
