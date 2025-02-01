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

    path("api/representante/", views.Api_RepresentanteGet, name="api-representante-get"),

    # path("api/representante/edit",   views.Api_RepresentanteEdit, name="api-representante-edit"),
]