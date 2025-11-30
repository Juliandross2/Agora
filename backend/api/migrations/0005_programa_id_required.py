# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_total_creditos_obligatorios'),
    ]

    operations = [
        # Primero eliminar cualquier configuración sin programa_id (si existiera)
        # En MySQL, Django nombra las FK como nombre_campo_id
        migrations.RunSQL(
            sql="DELETE FROM configuracion_elegibilidad WHERE programa_id_id IS NULL;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        
        # Luego hacer el campo NOT NULL
        migrations.AlterField(
            model_name='configuracionelegibilidad',
            name='programa_id',
            field=models.ForeignKey(
                help_text='Programa académico asociado (requerido)',
                on_delete=django.db.models.deletion.CASCADE,
                to='api.programa'
            ),
        ),
    ]

