# Generated by Django 5.1.6 on 2025-03-19 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Izelapp', '0003_alter_usuario_email_alter_usuario_tipo_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rh',
            field=models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3),
        ),
    ]
