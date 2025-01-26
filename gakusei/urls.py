from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sensei/", views.SenseiListView.as_view(), name="sensei"),
    path("sensei/<int:pk>", views.SenseiDetailView.as_view(), name="sensei-detail"),
    path("sensei/registrar", views.SenseiCreateView.as_view(), name="sensei-create"),
]