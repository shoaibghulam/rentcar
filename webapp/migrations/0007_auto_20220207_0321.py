# Generated by Django 3.2.11 on 2022-02-06 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_ordersmodel_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewsmodel',
            old_name='starts',
            new_name='stars',
        ),
        migrations.AlterField(
            model_name='carsmodel',
            name='status',
            field=models.TextField(choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')], default='In Progress', max_length=200),
        ),
    ]
