# Generated by Django 3.2.4 on 2021-06-26 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wsite', '0007_auto_20210626_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='_contact',
            new_name='contact',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='_status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='_user',
            new_name='user',
        ),
    ]
