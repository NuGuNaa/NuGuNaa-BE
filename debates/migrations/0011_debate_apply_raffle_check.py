# Generated by Django 5.0.1 on 2024-02-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debates', '0010_alter_debate_apply_petition_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='debate_apply',
            name='raffle_check',
            field=models.BooleanField(null=True),
        ),
    ]
