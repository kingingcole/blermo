# Generated by Django 2.1 on 2019-01-07 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='body',
        ),
    ]
