# Generated by Django 3.1.7 on 2021-04-19 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_auto_20210322_2049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlist',
            old_name='questionScore',
            new_name='answerCount',
        ),
    ]
