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
    path("asistencia/registrar-rezagados", views.AsistenciaCreateRezagados, name="asistencia-create-rezagados"),


    path("pagos/", views.PagosListView.as_view(), name="pagos"),
    path("pagos/<int:pk>", views.PagosDetailView.as_view(), name="pagos-detail"),
    path("pagos/registrar", views.PagosCreateView.as_view(), name="pagos-create"),


    path("solvencias/", views.SolvenciaClaseListView.as_view(), name="solvencias-clase"),
    path("solvencias/clase-<int:pk>", views.SolvenciaClaseDetailView.as_view(), name="solvencias-clase-detail"),


    path("sedes/", views.SedeListView.as_view(), name="sede"),
    path("sedes/<int:pk>", views.SedeDetailView.as_view(), name="sede-detail"),
    path("sedes/registrar", views.SedeCreateView.as_view(), name="sede-create"),


    path("cursos/", views.CursoListView.as_view(), name="curso"),
    path("cursos/<int:pk>", views.CursoDetailView.as_view(), name="curso-detail"),
    path("cursos/registrar", views.CursoCreateView.as_view(), name="curso-create"),


    path("metodosdepago/", views.MetodosPagoListView.as_view(), name="metodos-pago"),
    path("metodosdepago/<int:pk>", views.MetodosPagoDetailView.as_view(), name="metodos-pago-detail"),
    path("metodosdepago/registrar", views.MetodosPagoCreateView.as_view(), name="metodos-pago-create"),


    path("descuentosespeciales/", views.DescuentoEspecialListView.as_view(), name="descuento-especial"),
    path("descuentosespeciales/<int:pk>", views.DescuentoEspecialDetailView.as_view(), name="descuento-especial-detail"),
    path("descuentosespeciales/registrar", views.DescuentoEspecialCreateView.as_view(), name="descuento-especial-create"),


    path("becas/", views.BecaListView.as_view(), name="becas"),
    path("becas/<int:pk>", views.BecaDetailView.as_view(), name="becas-detail"),
    path("becas/registrar", views.BecaCreateView.as_view(), name="becas-create"),
    path("becas/asignar", views.BecaAssingView.as_view(), name="becas-asignar"),


    # API
    path("api/representantes/", views.Api_RepresentantesGet, name="api-representantes-get"),
    path("api/clase/", views.Api_ClaseGet, name="api-clase-get"),
    path("api/estudiante/", views.Api_EstudianteGet, name="api-estudiante-get"),

    path("api/diasdeclase/form", views.Api_DiasDeClase_Form, name="api-dia-de-clase-form"),

    path("api/asistencia/form", views.Api_AsistenciaForm, name="api-asistencia-form"),
    path("api/asistencia/form-rezagados/", views.Api_AsistenciaFormRezagados, name="api-asistencia-form-rezagados"),


    path("api/pagos/clases/", views.Api_Pagos_Clases, name="api-pagos-clases"),
    path("api/pagos/mensualidad/", views.Api_Pagos_Mensualidad, name="api-pagos-mensualidad"),
    
    
]