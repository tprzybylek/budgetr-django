# Generated by Django 2.0.7 on 2018-07-17 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_remove_category_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budget',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='user_id',
            new_name='user',
        ),
    ]
