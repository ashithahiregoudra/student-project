from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('result_analysis', '0014_alter_bookmark_unique_together_bookmark_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='course',
            field=models.ForeignKey(null=True, on_delete=models.CASCADE, to='result_analysis.course'),
        ),
    ]