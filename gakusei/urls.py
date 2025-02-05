from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("sensei/", views.SenseiListView.as_view(), name="sensei"),
    path("sensei/<int:pk>", views.SenseiDetailView.as_view(), name="sensei-detail"),
    path("sensei/registrar", views.SenseiCreateView.as_view(), name="sensei-create"),

    path("estudiante/", views.EstudianteListView.as_view(), name="estudiante"),
    path("estudiante/<int:pk>", views.EstudianteDetailView.as_view(), name="estudiante-detail"),
    path("estudiante/registrar", views.EstudianteCreateView.as_view(), name="estudiante-create"),
    path("estudiante/registrar/representante", views.RepresentanteCreatePopup.as_view(), name="estudiante-create-representante"),

    path("representante/registrar", views.RepresentanteCreateView.as_view(), name="representante-create"),

    path("clase/", views.ClaseListView.as_view(), name="clase"),
    path("clase/<int:pk>", views.ClaseDetailView.as_view(), name="clase-detail"),
    path("clase/registrar", views.ClaseCreateView.as_view(), name="clase-create"),

    path("horario/", views.HorarioListView.as_view(), name="horario"),
    path("horario/<int:pk>", views.HorarioDetailView.as_view(), name="horario-detail"),
    path("horario/registrar", views.HorarioCreateView.as_view(), name="horario-create"),


    path("inscripciones/", views.InscripcionesListView.as_view(), name="inscripciones"),
    path("inscripciones/<int:pk>", views.InscripcionesDetailView.as_view(), name="inscripciones-detail"),
    path("inscripciones/registrar", views.InscripcionesCreateView.as_view(), name="inscripciones-create"),

    path("diadeclase/", views.DiaDeClaseListView.as_view(), name="dia-de-clase"),
    path("diadeclase/<int:pk>", views.DiaDeClaseDetailView.as_view(), name="dia-de-clase-detail"),
    path("diadeclase/registrar", views.DiaDeClaseCreateView.as_view(), name="dia-de-clase-create"),

    path("asistencia/", views.AsistenciaListView.as_view(), name="asistencia"),
    path("asistencia/<int:pk>", views.AsistenciaDetailView.as_view(), name="asistencia-detail"),
    path("asistencia/registrar", views.AsistenciaCreate, name="asistencia-create"),
    path("asistencia/registrar-clasic", views.AsistenciaCreateView.as_view(), name="asistencia-create-clasic"),


    path("api/representantes/", views.Api_RepresentantesGet, name="api-representantes-get"),
    path("api/clase/", views.Api_ClaseGet, name="api-clase-get"),
    path("api/estudiante/", views.Api_EstudianteGet, name="api-estudiante-get"),

    path("api/clase/diadeclase/", views.Api_DiaDeClaseGet, name="api-clase-diadeclase-get"),
    path("api/diadeclase/estudiantes", views.Api_EstudiantesInscriptosGet, name="api-inscripciones-estudiantes-get"),
    

    path("api/diadeclase/estudiantes_clasic", views.Api_EstudiantesInscriptosGetClasic, name="api-inscripciones-estudiantes-get-clasic"),
    # path("api/representante/edit",   views.Api_RepresentanteEdit, name="api-representante-edit"),
]