from .models import Solvencias, Clase

from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

def solvencias_generator():

    try:
        # Se generan las Solvencias solo de las Clases Activas
        clases_activas = Clase.objects.filter(status=Clase.Status.ACTIVO)

        # Obtenemos las clases activas, las inscripciones de cada uno y revisamos sus solvencias
        for clase in clases_activas:

            inscripciones = clase.inscripciones.all()

            # Fechas para buscar/generar las solvencias
            ahora = now().date()+relativedelta(day=1)
            f_inicio = clase.f_inicio+relativedelta(day=1)

            # Direferencia de meses
            dif = relativedelta(ahora, f_inicio)
            meses = dif.years*12 + dif.months

            # Por cada Estudiante Incrito en una Clase, itera para revisar sus solvencias
            for inscrito in inscripciones:

                # Se agrega un +1 para que cuente el mes inicial de la clase
                for i in range(meses+1):
                    mes_actual = f_inicio+relativedelta(months=+i)

                    sol_nueva, sol_creado = Solvencias.objects.get_or_create(
                            estudiante = inscrito.estudiante,
                            clase = clase,
                            mes = mes_actual,

                            defaults={
                                "pagado": Solvencias.Pagado.SIN_PAGAR,
                                "monto_a_pagar": inscrito.precio_a_pagar,
                                "obs": "SOLVENCIA GENERADA AUTOMATICAMENTE",
                            }
                        )

        return (True, "Solvencias Generadas Correctamente.")
    
    except:
        return (False, "Error al Generar Solvencias")

