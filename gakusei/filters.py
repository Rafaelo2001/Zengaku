from .models import Sensei, Estudiante, Clase
from django import forms
import django_filters

from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django.db.models import Q

class SenseiFilter(django_filters.FilterSet):
    class Meta:
        model = Sensei
        
        fields = ["status","personal_data__cedula", "nombres", "apellidos", "personal_data__telefono", "personal_data__personal_email", "institucional_email", "EN_level", "JP_level",] 

    status = django_filters.ChoiceFilter(choices=Sensei.Status , widget=forms.RadioSelect, empty_label="Cualquier Status")
    JP_level = django_filters.ChoiceFilter(choices=Sensei.JP_Levels , widget=forms.RadioSelect, empty_label="Cualquier Nivel")
    EN_level = django_filters.ChoiceFilter(choices=Sensei.EN_Levels , widget=forms.RadioSelect, empty_label="Cualquier Nivel")

    personal_data__cedula           = django_filters.NumberFilter(lookup_expr="icontains", label="Cédula", widget=forms.NumberInput(attrs={"max":"999999999", "step":1}))
    personal_data__personal_email   = django_filters.CharFilter(lookup_expr="icontains",   label="Correo Personal",      widget=forms.EmailInput)
    personal_data__telefono         = django_filters.CharFilter(lookup_expr="icontains",   label="Telefono Movil",       widget=forms.TextInput(attrs={"type":"tel", "maxlength":12}))
    institucional_email             = django_filters.CharFilter(lookup_expr="icontains",   label="Correo Institucional", widget=forms.EmailInput)

    nombres = django_filters.CharFilter(method="filter_nombres", label="Nombres")
    apellidos = django_filters.CharFilter(method="filter_apellidos", label="Apellidos")


    def filter_nombres(self, queryset, name, value):

        return queryset.annotate(
            nombres = Concat("personal_data__first_name", Value(" "), "personal_data__middle_name", output_field=CharField())
        ).filter(Q(personal_data__first_name__icontains=value) | Q(personal_data__middle_name__icontains=value) | Q(nombres__icontains=value))


    def filter_apellidos(self, queryset, name, value):
        return queryset.annotate(
            apellidos = Concat("personal_data__last_name_1", Value(" "), "personal_data__last_name_2", output_field=CharField())
        ).filter(Q(personal_data__last_name_1__icontains=value) | Q(personal_data__last_name_2__icontains=value) | Q(apellidos__icontains=value))



class EstudianteFilter(django_filters.FilterSet):
    class Meta:
        model = Estudiante
        fields = ["status","personal_data__cedula", "nombres", "apellidos", "personal_data__telefono", "personal_data__personal_email",] 

    status = django_filters.ChoiceFilter(choices=Estudiante.Status , widget=forms.RadioSelect, empty_label="Cualquier Status")
    
    personal_data__cedula           = django_filters.NumberFilter(lookup_expr="icontains", label="Cédula", widget=forms.NumberInput(attrs={"max":"999999999", "step":1}))
    personal_data__personal_email   = django_filters.CharFilter(lookup_expr="icontains",   label="Correo Personal", widget=forms.EmailInput)
    personal_data__telefono         = django_filters.CharFilter(lookup_expr="icontains",   label="Telefono Movil",  widget=forms.TextInput(attrs={"type":"tel", "maxlength":12}))

    nombres = django_filters.CharFilter(method="filter_nombres", label="Nombres")
    apellidos = django_filters.CharFilter(method="filter_apellidos", label="Apellidos")


    def filter_nombres(self, queryset, name, value):

        return queryset.annotate(
            nombres = Concat("personal_data__first_name", Value(" "), "personal_data__middle_name", output_field=CharField())
        ).filter(Q(personal_data__first_name__icontains=value) | Q(personal_data__middle_name__icontains=value) | Q(nombres__icontains=value))


    def filter_apellidos(self, queryset, name, value):
        return queryset.annotate(
            apellidos = Concat("personal_data__last_name_1", Value(" "), "personal_data__last_name_2", output_field=CharField())
        ).filter(Q(personal_data__last_name_1__icontains=value) | Q(personal_data__last_name_2__icontains=value) | Q(apellidos__icontains=value))



class ClaseFilter(django_filters.FilterSet):
    class Meta:
        model = Clase
        fields = ["status", "curso", "sensei", "sede", "f_inicio", "f_inicio__lt", "f_inicio__gt", "f_cierre", "f_cierre__gt", "f_cierre__lt", "horas_semanales", "precio", "precio__gt", "precio__lt",  "individual", ]

    status = django_filters.ChoiceFilter(choices=Clase.Status , widget=forms.RadioSelect, empty_label="Cualquier Status")
    individual = django_filters.ChoiceFilter(
        widget=forms.RadioSelect, empty_label="Cualquiera", 
        choices=[
            (True, "Si"),
            (False, "No"),
        ]
    )

    precio     = django_filters.NumberFilter(field_name="precio", label="Precio Exacto ($)")
    precio__gt = django_filters.NumberFilter(field_name="precio", label="Mayor a Precio ($)", lookup_expr="gt")
    precio__lt = django_filters.NumberFilter(field_name="precio", label="Menor a Precio ($)", lookup_expr="lt")

    f_inicio     = django_filters.DateFilter(field_name="f_inicio", label="Fecha de Inicio Exacta",     widget=forms.DateInput(attrs={"type":"date"}))
    f_inicio__gt = django_filters.DateFilter(field_name="f_inicio", label="Después de Fecha de Inicio", widget=forms.DateInput(attrs={"type":"date"}), lookup_expr="gt")
    f_inicio__lt = django_filters.DateFilter(field_name="f_inicio", label="Antes de Fecha de Inicio",   widget=forms.DateInput(attrs={"type":"date"}), lookup_expr="lt")

    f_cierre     = django_filters.DateFilter(field_name="f_cierre", label="Fecha de Cierre Exacta",     widget=forms.DateInput(attrs={"type":"date"}))
    f_cierre__gt = django_filters.DateFilter(field_name="f_cierre", label="Después de Fecha de Cierre", widget=forms.DateInput(attrs={"type":"date"}), lookup_expr="gt")
    f_cierre__lt = django_filters.DateFilter(field_name="f_cierre", label="Antes de Fecha de Cierre",   widget=forms.DateInput(attrs={"type":"date"}), lookup_expr="lt")

