# Generated by Django 3.2.11 on 2022-02-06 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20220207_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewsmodel',
            name='starts',
            field=models.IntegerField(default=0),
        ),
    ]