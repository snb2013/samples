# Generated by Django 2.1 on 2018-10-13 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_auto_20181013_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='parent_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='chatbot.Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='parent_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='chatbot.Answer'),
        ),
    ]