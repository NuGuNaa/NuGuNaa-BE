# Generated by Django 5.0.1 on 2024-02-01 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0004_remove_petition_file_bill_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='petition_file',
            name='petition_file',
        ),
        migrations.AddField(
            model_name='petition_file',
            name='petition_file_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='petition_file',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
