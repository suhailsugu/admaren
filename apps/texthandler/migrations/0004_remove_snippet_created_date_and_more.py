# Generated by Django 5.0.2 on 2024-04-21 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texthandler', '0003_alter_snippet_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='modified_date',
        ),
        migrations.AddField(
            model_name='snippet',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='timestamp'),
        ),
    ]
