from django.db import models

from django.core.validators import RegexValidator

# PERSONAS
class Persona(models.Model):

    cedula = models.CharField(
        "Cédula",
        max_length = 10,
        unique     = True,
        validators = [RegexValidator('^[V|E|J|P][0-9]{5,9}$', 'La cédula debe tener el formato V123456789.')]
    )
    
    first_name  = models.CharField("Primer Nombre", max_length=255)
    middle_name	= models.CharField("Segundo Nombre", max_length=255, blank=True)
    last_name_1	= models.CharField("Primer Apellido", max_length=255)
    last_name_2 = models.CharField("Segundo Apellido", max_length=255, blank=True)
    
    personal_email = models.EmailField("Correo Personal", max_length=254)
    telefono  = models.CharField(
        "Teléfono Movil",
        max_length = 12,
        validators = [RegexValidator("^(0414|0424|0412|0416|0426)[-][0-9]{7}$", "El teléfono debe tener el formato 04XX-1234567")]
    )

    def full_name(self):
        name = (self.first_name + " ")

        if self.middle_name:
            name += (self.middle_name[0] + " ")

        name += self.last_name_1

        if self.last_name_2:
            name += (" " + self.last_name_2[0])

        return name


    def __str__(self):

        name = (self.first_name + " ")

        if self.middle_name:
            name += (self.middle_name[0] + " ")

        name += self.last_name_1

        if self.last_name_2:
            name += (" " + self.last_name_2[0])

        return f"{self.cedula} - {name}"


class Sensei(models.Model):

    class EN_Levels(models.TextChoices):
        A1 = "A1"
        A2 = "A2"
        B1 = "B1"
        B2 = "B2"
        C1 = "C1"
        C2 = "C2"

    class JP_Levels(models.TextChoices):
        N5 = "N5"
        N4 = "N4"
        N3 = "N3"
        N2 = "N2"
        N1 = "N1"

    class Status(models.TextChoices):
        ACTIVO  = "Activo"
        RETIRADO = "Retirado"

    personal_data = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="sensei")

    institucional_email = models.EmailField("Correo Institucional", max_length=254)
    EN_level = models.CharField("Nivel de Inglés", max_length=2, choices=EN_Levels, default=EN_Levels.B1)
    JP_level = models.CharField("Nivel de Japonés", max_length=2, choices=JP_Levels, default=JP_Levels.N4)

    status = models.CharField("Status", max_length=10, choices=Status, default=Status.ACTIVO)

    def __str__(self):
        return self.personal_data.__str__()


class Representante(models.Model):
    personal_data = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="representante")

    def __str__(self):
        return self.personal_data.__str__()


class Estudiante(models.Model):

    class Status(models.TextChoices):
        ACTIVO  = "Activo"
        RETIRADO = "Retirado"

    personal_data = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="estudiante")
    representante = models.ForeignKey(Representante, blank=True, null=True, on_delete=models.SET_NULL, default=None)
    status = models.CharField("Status", max_length=10, choices=Status, default=Status.ACTIVO)

    def __str__(self):
        return self.personal_data.__str__()



# CLASES
class Curso(models.Model):
    modulo = models.CharField("Módulo", max_length=50, unique=True)

    def __str__(self):
        return self.modulo


class Sede(models.Model):
    nombre = models.CharField(max_length=50)
    ubicacion = models.TextField("Ubicación")
    contacto = models.TextField("Formas de Contacto")

    # Usar el link (src) que viene en el iframe de insertar un mapa
    maps = models.URLField("Google Maps", max_length=500, blank=True)

    def __str__(self):
        return self.nombre


class Clase(models.Model):

    class Status(models.TextChoices):
        ACTIVO     = "Activa"
        PAUSADO    = "En Pausa"
        SUSPENDIDO = "Suspendida"
        COMPLETADO = "Terminanda"

    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name="clases")
    sensei = models.ForeignKey(Sensei, on_delete=models.SET_NULL, null=True, related_name="clases")
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name="clases")

    f_inicio = models.DateField("Fecha de Inicio")
    horas_semanales = models.PositiveSmallIntegerField("Horas (min) Semanales")
    precio = models.PositiveSmallIntegerField()

    status = models.CharField(max_length=10, choices=Status, default=Status.ACTIVO)

    def __str__(self):
        sensei = self.sensei.personal_data.full_name()

        modulo = self.curso

        sede = self.sede


        return f"{modulo} {sede} - {sensei}"


class Horario(models.Model):

    class Weekdays(models.TextChoices):
        LUNES     = "Lunes"
        MARTES    = "Martes"
        MIERCOLES = "Miercoles"
        JUEVES    = "Jueves"
        VIERNES   = "Viernes"
        SABADO    = "Sábado"
        DOMINGO   = "Domingo"

    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="horario")

    dia_semana = models.CharField("Dia de la Semana", max_length=10, choices=Weekdays)
    hora_entrada = models.TimeField()
    hora_salida  = models.TimeField()


    def __str__(self):
        clase = self.clase

        dia = self.dia_semana
        entrada = self.hora_entrada
        salida = self.hora_salida

        return f"{clase} - {dia} de {entrada} a {salida}"



# BECAS
class Becas(models.Model):
    class TipoDescuento(models.TextChoices):
        PORCENTUAL = "Porcentual"
        CARDINAL   = "Cardinal"

    class Status(models.TextChoices):
        ACTIVO = "Activo"
        DESABILITADO = "Deshabilitado"

    nombre = models.CharField(max_length=200)
    descuento = models.PositiveSmallIntegerField()
    tipo_descuento = models.CharField("Tipo de Descuento", max_length=10, choices=TipoDescuento, default=TipoDescuento.PORCENTUAL)
    status = models.CharField(max_length=15, choices=Status, default=Status.ACTIVO)


class Becados(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, related_name="beca")
    beca = models.ForeignKey(Becas, on_delete=models.CASCADE, related_name="becados")
    obs = models.TextField("Observaciones", blank=True)


class DescuentoEspecial(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, related_name="descuento")
    descuento = models.PositiveSmallIntegerField()
    obs = models.TextField("Observaciones", blank=True)



# PAGOS
class MetodosPagos(models.Model):
    metodo = models.CharField("Método", max_length=255)
    datos = models.TextField("Datos de Pago")
    obs = models.TextField("Observaciones")


class Pagos(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="pagos")
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="pagos")
    metodo = models.ForeignKey(MetodosPagos, on_delete=models.CASCADE, related_name="pagos")
    monto_pagado = models.PositiveSmallIntegerField()
    referencia = models.CharField(max_length=255)
    obs = models.TextField("Observaciones")


class Solvencias(models.Model):

    class Pagado(models.TextChoices):
        PAGADO    = "Pagado"
        ABONADO   = "Abonado"
        SIN_PAGAR = "Sin Pagar"

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="solvencias")
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="solvencias")

    # En el mes se guardaran principalmente el Año y el Mes, el Dia siempre sera 1.
    mes = models.DateField()
    
    pagado = models.CharField(max_length=10, choices=Pagado, default=Pagado.SIN_PAGAR)
    monto_a_pagar = models.PositiveSmallIntegerField()
    monto_abonado = models.PositiveSmallIntegerField(default=0)
    obs = models.TextField("Observaciones")


class Comprobantes(models.Model):
    pagos = models.ForeignKey(Pagos, on_delete=models.CASCADE, related_name="comprobantes")
    solvencias = models.ForeignKey(Solvencias, on_delete=models.CASCADE, related_name="comprobantes")

    monto_aplicado = models.PositiveSmallIntegerField()



# ASISTENCIAS
class DiaDeClase(models.Model):
    class Status(models.TextChoices):
        IMPARTIDA  = "Impartida"
        SUSPENDIDA = "Suspendida"
        CANCELADA  = "Cancelada"

    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name="dias_de_clase")
    numero = models.PositiveSmallIntegerField("Número de Clase")
    fecha = models.DateField()
    status = models.CharField(max_length=10, choices=Status, default=Status.IMPARTIDA)
    obs = models.TextField("Observaciones", blank=True)


class Asistencias(models.Model):
    dia_clase = models.ForeignKey(DiaDeClase, on_delete=models.CASCADE, related_name="asistencias")
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="asistencias")
    presente = models.BooleanField(default=False)
