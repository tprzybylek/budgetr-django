# Generated by Django 2.0.7 on 2018-07-17 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_auto_20180717_1336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='parent_id',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='operation',
            old_name='budget_id',
            new_name='budget',
        ),
        migrations.RenameField(
            model_name='operation',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='operation',
            old_name='user_id',
            new_name='user',
        ),
    ]
