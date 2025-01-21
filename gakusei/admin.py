from django.contrib import admin

from .models import Persona, Sensei, Estudiante, Representante
from .models import Curso, Sede, Clase, Horario

# Register your models here.
admin.site.register(Persona)
admin.site.register(Sensei)
admin.site.register(Estudiante)
admin.site.register(Representante)

admin.site.register(Curso)
admin.site.register(Sede)
admin.site.register(Clase)
admin.site.register(Horario)
