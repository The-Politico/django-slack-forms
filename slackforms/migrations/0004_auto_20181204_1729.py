# Generated by Django 2.1.4 on 2018-12-04 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slackforms', '0003_auto_20181204_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='form',
            old_name='argument_name',
            new_name='argument_prop_name',
        ),
    ]
