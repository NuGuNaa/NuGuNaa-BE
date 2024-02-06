# Generated by Django 5.0.1 on 2024-02-05 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debates', '0007_alter_debate_apply_position'),
        ('petitions', '0005_remove_petition_file_petition_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debate_apply',
            name='petition_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petitions.petition'),
        ),
    ]