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

    # path("api/representante/create", views.Api_RespresentanteRegistro, name="api-representante-create"),
    # path("api/representante/edit",   views.Api_RepresentanteEdit, name="api-representante-edit"),
]