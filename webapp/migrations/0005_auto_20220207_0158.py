# Generated by Django 3.2.11 on 2022-02-06 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_reviewsmodel_starts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewsmodel',
            name='carid',
        ),
        migrations.AddField(
            model_name='reviewsmodel',
            name='status',
            field=models.CharField(default='No', max_length=100),
        ),
    ]
