# Generated by Django 3.2.8 on 2021-11-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_usermovie_bought'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermovie',
            name='rating',
            field=models.FloatField(max_length=5, null=True),
        ),
    ]
