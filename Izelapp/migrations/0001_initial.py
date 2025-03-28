# Generated by Django 4.2.6 on 2025-03-26 20:43

import Izelapp.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cita', models.DateField()),
                ('hora_cita', models.TimeField()),
                ('estado_cita', models.CharField(choices=[('agendada', 'Agendada'), ('atendida', 'Atendida'), ('cancelada', 'Cancelada'), ('NA', 'No atendida')], default='Agendada', max_length=10)),
                ('especialidad', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tratamiento', models.TextField(max_length=200)),
                ('diagnostico', models.TextField(max_length=200)),
                ('motivo_consulta', models.TextField(max_length=200)),
                ('fecha_consulta', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contratacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_contratacion', models.DateField()),
                ('hoja_vida', models.FileField(blank=True, null=True, upload_to='hojas_vida/')),
                ('contrato', models.FileField(blank=True, null=True, upload_to='contratos/')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('tipo_doc', models.CharField(choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería')], max_length=20)),
                ('num_doc', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('genero', models.CharField(choices=[('masculino', 'MASCULINO'), ('femenino', 'FEMENINO'), ('prefiero no decirlo', 'PREFIERO NO DECIRLO')], max_length=20)),
                ('rh', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('telefono', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('tipo_poblacion', models.CharField(max_length=50)),
                ('ocupacion', models.CharField(max_length=20)),
                ('eps', models.CharField(max_length=20)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to=Izelapp.models.user_directory_path, verbose_name='Imagen')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rol_acceso', models.CharField(max_length=100)),
                ('centro_administracion', models.CharField(max_length=255)),
                ('permisos', models.JSONField()),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('Izelapp.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Auxiliar',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('departamento', models.CharField(max_length=100)),
                ('supervisor', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('Izelapp.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('especialidad', models.CharField(max_length=100)),
                ('numero_registro_profesional', models.CharField(max_length=50)),
                ('licencia_certificacion', models.BooleanField(default=False)),
                ('fecha_contratacion', models.DateField()),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('Izelapp.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('regimen', models.CharField(choices=[('subcidiado', 'SUBSIDIADO'), ('contributivo', 'CONTRIBUTIVO'), ('otro', 'OTRO')], max_length=30)),
                ('numero_seguro_social', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('Izelapp.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TI',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('Izelapp.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RecetaMedica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicamento', models.CharField(max_length=100)),
                ('concentracion', models.CharField(max_length=100)),
                ('duracion', models.CharField(max_length=100)),
                ('cantidad', models.CharField(max_length=100)),
                ('via_administracion', models.CharField(max_length=20)),
                ('diagnostico_principal', models.TextField(max_length=255)),
                ('diagnostico_relacionados', models.TextField(max_length=255)),
                ('intervalo', models.CharField(max_length=20)),
                ('recomendaciones', models.CharField(max_length=255)),
                ('indicaciones', models.CharField(max_length=255)),
                ('fecha_medicado', models.DateField(auto_now=True)),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recetas', to='Izelapp.cita')),
            ],
        ),
        migrations.CreateModel(
            name='PerfilPaciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tratamiento', models.TextField(max_length=200, null=True)),
                ('vida_sexual', models.CharField(choices=[('activo', 'ACTIVO'), ('no activo', 'NO ACTIVO')], max_length=50)),
                ('ciclo_mestrual', models.TextField(max_length=200, null=True)),
                ('sustancias_psicotivas', models.BooleanField(default=False)),
                ('habitos_alimenticios', models.TextField(max_length=200, null=True)),
                ('consumo_alcohol', models.BooleanField(default=False)),
                ('habito_sueño', models.TextField(max_length=200, null=True)),
                ('antecedentes_personales', models.TextField(max_length=200, null=True)),
                ('consulta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfiles', to='Izelapp.consulta')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenMedica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad_referido', models.CharField(max_length=255)),
                ('motivo', models.CharField(max_length=255)),
                ('fecha_ordenado', models.DateField(auto_now=True)),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordenes', to='Izelapp.cita')),
            ],
        ),
        migrations.CreateModel(
            name='CertificadoIncapacidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dias_incapacidad', models.CharField(max_length=2)),
                ('motivo_incapacidad', models.CharField(max_length=255)),
                ('fecha_emision', models.DateField(auto_now=True)),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificados', to='Izelapp.cita')),
            ],
        ),
        migrations.CreateModel(
            name='Vacuna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_vacuna', models.CharField(max_length=150)),
                ('fecha_aplicacion', models.DateField()),
                ('dosis', models.CharField(max_length=100)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacunas', to='Izelapp.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioMedico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(choices=[('lunes', 'Lunes'), ('martes', 'Martes'), ('miercoles', 'Miércoles'), ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sabado', 'Sábado'), ('domingo', 'Domingo')], default='lunes', max_length=10)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Izelapp.medico')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriaClinica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ultima_atencion', models.DateField()),
                ('tratamiento', models.TextField()),
                ('notas', models.TextField()),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Izelapp.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Disponibilidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('tipo_cita', models.CharField(choices=[('general', 'General'), ('odontologia', 'Odontología')], max_length=50)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Izelapp.medico')),
            ],
        ),
        migrations.CreateModel(
            name='DatoQuirurgico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_cirugia', models.CharField(max_length=150)),
                ('fecha_cirugia', models.DateField()),
                ('complicaciones', models.TextField(max_length=200)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datos_quirurgicos', to='Izelapp.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='DatoAntropometrico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('altura_decimal', models.DecimalField(decimal_places=2, max_digits=20)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=20)),
                ('indice_masa_corporal', models.DecimalField(decimal_places=2, max_digits=20)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datos_antropometricos', to='Izelapp.paciente')),
            ],
        ),
        migrations.AddField(
            model_name='consulta',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='Izelapp.paciente'),
        ),
        migrations.AddField(
            model_name='cita',
            name='medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medico_citas', to='Izelapp.medico'),
        ),
        migrations.AddField(
            model_name='cita',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paciente_agenda_cita', to='Izelapp.paciente'),
        ),
        migrations.CreateModel(
            name='Antecedente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(max_length=200, null=True)),
                ('tipo_antecedente', models.TextField(max_length=200)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='antecedentes', to='Izelapp.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='AgendaMedica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.TimeField()),
                ('motivo', models.CharField(max_length=200)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medico_agenda', to='Izelapp.medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paciente_cita', to='Izelapp.paciente')),
            ],
        ),
    ]
