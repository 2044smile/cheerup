# Generated by Django 5.0.6 on 2024-07-07 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_post_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]