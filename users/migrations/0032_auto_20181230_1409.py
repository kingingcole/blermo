# Generated by Django 2.1 on 2018-12-30 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_auto_20181219_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, related_name='follows', to='users.Profile'),
        ),
    ]
