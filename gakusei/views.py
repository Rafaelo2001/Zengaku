from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from json import loads

from django import forms
from .models import Sensei, Estudiante, Representante, Clase, Horario
from .forms import SenseiForm, EstudianteForm, RepresentanteForm

from django.views.generic import ListView, DetailView, FormView, CreateView

# Create your views here.
def index(request):
    return render(request, "gakusei/index.html")


# Sensei
sensei_templates = "gakusei/sensei/"
class SenseiListView(ListView):
    model = Sensei
    template_name = sensei_templates + "list.html"

class SenseiDetailView(DetailView):
    model = Sensei
    template_name = sensei_templates + "detail.html"


class SenseiCreateView(FormView):
    form_class = SenseiForm
    template_name = sensei_templates + "create.html"

    success_url = reverse_lazy("sensei")

    def form_valid(self, form):
        sensei = form.save()

        return HttpResponseRedirect(reverse("sensei-detail", kwargs={"pk":sensei.pk}))
    

# Estudiante
estudiante_templates = "gakusei/estudiante/"
class EstudianteListView(ListView):
    model = Estudiante
    template_name = estudiante_templates + "list.html"


class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = estudiante_templates + "detail.html"


class EstudianteCreateView(FormView):
    form_class = EstudianteForm
    template_name = estudiante_templates + "create.html"

    success_url = reverse_lazy("estudiante")

    def form_valid(self, form):
        estudiante = form.save()

        return HttpResponseRedirect(reverse("estudiante-detail", kwargs={"pk":estudiante.pk}))
    
    
# Representante
representante_templates = "gakusei/representante/"
class RepresentanteCreateView(FormView):
    form_class = RepresentanteForm
    template_name = representante_templates + "create.html"

    success_url = reverse_lazy("index")

    def form_valid(self, form):
        estudiante = form.save()

        return HttpResponseRedirect(reverse("estudiante-detail", kwargs={"pk":estudiante.pk}))
    

class RepresentanteCreatePopup(FormView):
    form_class = RepresentanteForm
    template_name = representante_templates + "create-popup.html"

    success_url = None

    def form_valid(self, form):
        representante = form.save()

        return JsonResponse({"id":  representante.pk,}, status=201)
    
    def form_invalid(self, form):
        return JsonResponse({"error_form": form.as_div()}, status=422)


# Clase
clase_templates = "gakusei/clase/"
class ClaseListView(ListView):
    model = Clase
    template_name = clase_templates + "list.html"


class ClaseDetailView(DetailView):
    model = Clase
    template_name = clase_templates + "detail.html"


class ClaseCreateView(CreateView):
    model = Clase
    fields = "__all__"
    template_name = clase_templates + "create.html"

    def get_success_url(self):
        return reverse("clase-detail", kwargs={"pk": self.object.pk})

    def get_form(self, form_class = None):

        form = super().get_form(form_class)

        form.fields["f_inicio"].widget = forms.DateInput(attrs={"type":"date"})
        form.fields["f_cierre"].widget = forms.DateInput(attrs={"type":"date"})

        return form



# Horario
horario_templates = "gakusei/horario/"
class HorarioListView(ListView):
    model = Horario
    template_name = horario_templates + "list.html"


class HorarioDetailView(DetailView):
    model = Horario
    template_name = horario_templates + "detail.html"


class HorarioCreateView(CreateView):
    model = Horario
    fields = "__all__"
    template_name = horario_templates + "create.html"

    def get_success_url(self):
        return reverse("horario-detail", kwargs={"pk": self.object.pk})

    def get_form(self, form_class = None):

        form = super().get_form(form_class)

        form.fields["hora_entrada"].widget = forms.TimeInput(attrs={"type":"time"})
        form.fields["hora_salida"].widget  = forms.TimeInput(attrs={"type":"time"})

        return form



# API
def Api_RepresentanteGet(request):
    raw_list = Representante.objects.all()

    refined_list = []

    for r in raw_list:
        refined_list.append({
            "id" : r.id, "text" : r.full_name(),
        })

    response = {
        "results": refined_list,
    }

    return JsonResponse(response, status=201)
