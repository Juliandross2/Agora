from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_configuracionelegibilidad_niveles_creditos_periodos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracionelegibilidad',
            name='porcentaje_avance_minimo',
        ),
    ]
