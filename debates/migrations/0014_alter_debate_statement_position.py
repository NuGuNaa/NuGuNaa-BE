# Generated by Django 5.0.1 on 2024-02-06 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debates', '0013_debate_statement_statement_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debate_statement',
            name='position',
            field=models.IntegerField(null=True),
        ),
    ]
