from django.db import models

from django.core.validators import RegexValidator

# PERSONAS
class Person(models.Model):

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

    personal_data = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="sensei")

    institucional_email = models.EmailField("Correo Institucional", max_length=254)
    EN_level = models.CharField("Nivel de Inglés", max_length=2, choices=EN_Levels, default=EN_Levels.B1)
    JP_level = models.CharField("Nivel de Japonés", max_length=2, choices=JP_Levels, default=JP_Levels.N4)

    status = models.CharField("Status", max_length=10, choices=Status, default=Status.ACTIVO)

    def __str__(self):
        return self.personal_data.__str__()


class Representante(models.Model):
    personal_data = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="representante")

    def __str__(self):
        return self.personal_data.__str__()


class Estudiante(models.Model):

    class Status(models.TextChoices):
        ACTIVO  = "Activo"
        RETIRADO = "Retirado"

    personal_data = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="estudiante")
    representante = models.ForeignKey(Representante, null=True, on_delete=models.SET_NULL, default=None)
    status = models.CharField("Status", max_length=10, choices=Status, default=Status.ACTIVO)

    def __str__(self):
        return self.personal_data.__str__()



# CLASES
class Curso(models.Model):
    modulo = models.CharField("Módulo", max_length=50)


class Sede(models.Model):
    nombre = models.CharField(max_length=50)
    ubicacion = models.TextField("Ubicación")
    contacto = models.TextField("Formas de Contacto")

    # Usar el link (src) que viene en el iframe de insertar un mapa
    maps = models.URLField("Google Maps", max_length=500, blank=True)


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


class Horario(models.Model):

    class Weekdays(models.TextChoices):
        LU = "Lunes"
        MA = "Martes"
        MI = "Miercoles"
        JU = "Jueves"
        VI = "Viernes"
        SA = "Sábado"
        DO = "Domingo"

    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="horario")

    dia_semana = models.CharField("Dia de la Semana", max_length=10, choices=Weekdays)
    hora_entrada = models.TimeField()
    hora_salida  = models.TimeField()



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



# ASISTENCIAS