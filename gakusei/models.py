from django.db import models

from django.core.validators import RegexValidator

# Create your models here.
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
        ACTIVE  = "Activo"
        RETIRED = "Retirado"

    personal_data = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="sensei")

    institucional_email = models.EmailField("Correo Institucional", max_length=254)
    EN_level = models.CharField("Nivel de Inglés", max_length=2, choices=EN_Levels, default=EN_Levels.B1)
    JP_level = models.CharField("Nivel de Japonés", max_length=2, choices=JP_Levels, default=JP_Levels.N4)

    status = models.CharField("Status", max_length=10, choices=Status, default=Status.ACTIVE)

    def __str__(self):
        return self.personal_data.__str__()


class Representante(models.Model):
    personal_data = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="representante")


class Estudiante(models.Model):

    class Status(models.TextChoices):
        ACTIVE  = "Activo"
        RETIRED = "Retirado"

    personal_data = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="estudiante")
    representante = models.ForeignKey(Representante, null=True, on_delete=models.SET_NULL, default=None)
    status = models.CharField("Status", max_length=10, choices=Status, default=Status.ACTIVE)

