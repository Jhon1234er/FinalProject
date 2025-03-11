# Generated by Django 4.2.6 on 2025-03-11 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Izelapp', '0002_usuario_imagen_alter_usuario_tipo_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo_doc',
            field=models.CharField(choices=[('CC', 'Cédula de Ciudadanía'), ('TI', 'Tarjeta de identidad'), ('CE', 'Cédula de Extranjería')], max_length=20),
        ),
    ]
