# Generated by Django 3.2.11 on 2022-03-10 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_carsmodel_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carsmodel',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.citymodels'),
        ),
    ]
