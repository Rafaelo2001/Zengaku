from django import forms

from django.db import transaction, IntegrityError

from .models import Persona, Sensei, Estudiante, Representante

class BasePersona(forms.Form):
    nacionalidad = forms.ChoiceField(
        choices=Persona.NACIONALITIES,
        initial=Persona.NACIONALITIES.VEN,
        widget=forms.RadioSelect(),
        required=True,
    )

    cedula = forms.IntegerField(
        label="Cédula",
        min_value=10000,
        max_value=999999999,
        widget=forms.NumberInput(attrs={"autofocus":True}),
    )

    def clean_cedula(self):
        ci = self.cleaned_data["cedula"]

        if Persona.objects.filter(cedula=ci).exists():
            self.add_error("cedula", "Esta cédula ya está registrada.") 

        return ci
    
    first_name  = forms.CharField(label="Primer Nombre", max_length=255)
    middle_name	= forms.CharField(label="Segundo Nombre", max_length=255, required=False)
    last_name_1	= forms.CharField(label="Primer Apellido", max_length=255)
    last_name_2 = forms.CharField(label="Segundo Apellido", max_length=255, required=False)

    telefono = forms.RegexField(
        label="Teléfono Movil", 
        max_length=12, 
        regex=r"^(0414|0424|0412|0416|0426)[-][0-9]{7}$",
        widget=forms.TextInput(attrs={"type":"tel"}),
    )

    personal_email = forms.EmailField(label="Correo Personal", max_length=254)


class SenseiForm(BasePersona):
    
    institucional_email = forms.EmailField(label="Correo Institucional", max_length=254)

    status = forms.ChoiceField(
        choices=Sensei.Status,
        widget=forms.RadioSelect(),
        initial=Sensei.Status.ACTIVO,
        required=True,
    )

    EN_level = forms.ChoiceField(
        label="Nivel de Inglés",
        choices=Sensei.EN_Levels,
        widget=forms.RadioSelect(),
        required=True,
    )

    JP_level = forms.ChoiceField(
        label="Nivel de Japonés",
        choices=Sensei.JP_Levels,
        widget=forms.RadioSelect(),
        required=True,
    )

    def save(self, commit=True):

        try:
            with transaction.atomic():
                
                personal_data = Persona.objects.create(
                    nacionalidad = self.cleaned_data.get("nacionalidad"),
                    cedula = self.cleaned_data.get("cedula"),
                    first_name = self.cleaned_data.get("first_name"),
                    middle_name = self.cleaned_data.get("middle_name"),
                    last_name_1 = self.cleaned_data.get("last_name_1"),
                    last_name_2 = self.cleaned_data.get("last_name_2"),
                    personal_email = self.cleaned_data.get("personal_email"),
                    telefono = self.cleaned_data.get("telefono"),
                )

                sensei = Sensei.objects.create(
                    personal_data = personal_data,
                    institucional_email = self.cleaned_data.get("institucional_email"),
                    EN_level = self.cleaned_data.get("EN_level"),
                    JP_level = self.cleaned_data.get("JP_level"),
                    status = self.cleaned_data.get("status"),
                )

        except Exception as e:
            self.add_error(None, f"Error al insertar datos en BDD: {e}")

        return sensei


class EstudianteForm(BasePersona):

    representante = forms.ModelChoiceField(Representante.objects.all())

    status = forms.ChoiceField(
        choices=Estudiante.Status,
        widget=forms.RadioSelect(),
        initial=Estudiante.Status.ACTIVO,
        required=True,
    )

    def save(self, commit=True):

        try:
            with transaction.atomic():
                
                personal_data = Persona.objects.create(
                    nacionalidad    = self.cleaned_data.get("nacionalidad"  ),
                    cedula          = self.cleaned_data.get("cedula"        ),
                    first_name      = self.cleaned_data.get("first_name"    ),
                    middle_name     = self.cleaned_data.get("middle_name"   ),
                    last_name_1     = self.cleaned_data.get("last_name_1"   ),
                    last_name_2     = self.cleaned_data.get("last_name_2"   ),
                    personal_email  = self.cleaned_data.get("personal_email"),
                    telefono        = self.cleaned_data.get("telefono"      ),
                )

                estudiante = Estudiante.objects.create(
                    personal_data = personal_data,
                    representante = self.cleaned_data.get("representante"),
                    status        = self.cleaned_data.get("status"),
                )

        except Exception as e:
            self.add_error(None, f"Error al insertar datos en BDD: {e}")

        return estudiante



# class RepresentanteForm(BasePersona):

#     def unpack(self, repre_obj:Representante):

#         self.initial["nacionalidad"]  = repre_obj.personal_data.nacionalidad
#         self.initial["cedula"]        = repre_obj.personal_data.cedula

#         self.initial["first_name"]  = repre_obj.personal_data.first_name
#         self.initial["middle_name"] = repre_obj.personal_data.middle_name
#         self.initial["last_name_1"] = repre_obj.personal_data.last_name_1
#         self.initial["last_name_2"] = repre_obj.personal_data.last_name_2
        
#         self.initial["telefono"]       = repre_obj.personal_data.telefono
#         self.initial["personal_email"] = repre_obj.personal_data.personal_email

    
#     def save(self, commit=True):

#         try:
#             with transaction.atomic():
                
#                 personal_data = Persona.objects.create(
#                     nacionalidad    = self.cleaned_data.get("nacionalidad"),
#                     cedula          = self.cleaned_data.get("cedula"),
#                     first_name      = self.cleaned_data.get("first_name"),
#                     middle_name     = self.cleaned_data.get("middle_name"),
#                     last_name_1     = self.cleaned_data.get("last_name_1"),
#                     last_name_2     = self.cleaned_data.get("last_name_2"),
#                     personal_email  = self.cleaned_data.get("personal_email"),
#                     telefono        = self.cleaned_data.get("telefono"),
#                 )

#                 representante = Representante.objects.create(
#                     personal_data = personal_data,
#                 )

#         except Exception as e:
#             self.add_error(None, f"Error al insertar datos en BDD: {e}")

#         return representante


#     def update(self, id):
#         try:
#             with transaction.atomic():

#                 representante = Representante.objects.get(pk=id)

#                 Persona.objects.filter(pk=representante.personal_data.id).update(
#                     nacionalidad    = self.cleaned_data.get("nacionalidad"),
#                     cedula          = self.cleaned_data.get("cedula"),
#                     first_name      = self.cleaned_data.get("first_name"),
#                     middle_name     = self.cleaned_data.get("middle_name"),
#                     last_name_1     = self.cleaned_data.get("last_name_1"),
#                     last_name_2     = self.cleaned_data.get("last_name_2"),
#                     personal_email  = self.cleaned_data.get("personal_email"),
#                     telefono        = self.cleaned_data.get("telefono"),
#                 )

#         except Exception as e:
#             self.add_error(None, f"Error al actualizar datos en BDD: {e}")

#         return representante

