import csv
import os
from django.apps import AppConfig
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError

class IzelappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Izelapp'

    def ready(self):
        from Izelapp.models import TablaReferenciaCIE10
        file_path = os.path.join(settings.BASE_DIR, 'Izelapp', 'data', 'cie10.txt')

        try:
            if TablaReferenciaCIE10.objects.exists():
                return  # Ya hay datos

            if not os.path.exists(file_path):
                print("Archivo CIE10 no encontrado:", file_path)
                return

            with open(file_path, encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')  # Cambia el delimitador si es necesario

                objs = []
                for row in reader:
                    if row.get('codigo') and row.get('descripcion'):
                        objs.append(TablaReferenciaCIE10(
                            codigo=row['codigo'].strip(),
                            descripcion=row['descripcion'].strip(),
                            tabla='CIE10'  # fijo si no viene en el archivo
                        ))

                TablaReferenciaCIE10.objects.bulk_create(objs)
                print(f"Importados {len(objs)} registros de CIE10")
        except (OperationalError, ProgrammingError):
            # Esto previene errores durante migraciones iniciales
            pass
