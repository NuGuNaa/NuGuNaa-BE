# Generated by Django 5.0.1 on 2024-02-05 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debates', '0003_debate_apply_id_alter_debate_apply_petition_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debate_apply',
            name='position',
            field=models.CharField(default='0', max_length=1),
        ),
    ]