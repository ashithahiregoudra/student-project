# Generated by Django 5.1.4 on 2025-01-06 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result_analysis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentscore',
            name='practice_sport',
        ),
        migrations.AlterField(
            model_name='studentscore',
            name='is_first_child',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='studentscore',
            name='math_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentscore',
            name='nr_siblings',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='studentscore',
            name='reading_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentscore',
            name='wkly_study_hours',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='studentscore',
            name='writing_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
