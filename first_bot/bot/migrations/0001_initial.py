# Generated by Django 4.0.3 on 2022-03-22 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.IntegerField(default=0)),
                ('choice_text', models.CharField(max_length=100)),
                ('answer_text', models.CharField(max_length=100)),
            ],
        ),
    ]
