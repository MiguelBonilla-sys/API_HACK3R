# Generated by Django 5.1.5 on 2025-06-05 03:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_auditlog_options_alter_conferencias_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Usuario que realizó la operación (NULL si el usuario fue eliminado)', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
