# Generated by Django 2.1.7 on 2019-02-23 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbt', '0007_auto_20190223_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='matric',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
