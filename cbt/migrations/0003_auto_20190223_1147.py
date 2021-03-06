# Generated by Django 2.1.7 on 2019-02-23 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cbt', '0002_auto_20190221_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.AddField(
            model_name='question',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='cbt.Course'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=500, verbose_name='Question'),
        ),
    ]
