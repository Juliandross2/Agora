from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_fix_programa_id_column_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracionelegibilidad',
            name='niveles_creditos_periodos',
        ),
    ]
