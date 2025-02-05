from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from json import loads

from django import forms
from django.forms.models import model_to_dict

from .models import Sensei, Estudiante, Representante, Clase, Horario, Inscripciones, DiaDeClase, Asistencias
from .forms import SenseiForm, EstudianteForm, RepresentanteForm, SeleccionAsistenciaForm, AsistenciaForm

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
    ordering = "clase"
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


# Inscripciones
inscripciones_templates = "gakusei/inscripciones/"

class InscripcionesListView(ListView):
    model = Inscripciones
    ordering = "clase"

    template_name = inscripciones_templates + "list.html"

class InscripcionesDetailView(DetailView):
    model = Inscripciones
    template_name = inscripciones_templates + "detail.html"

class InscripcionesCreateView(CreateView):
    model = Inscripciones
    fields = "__all__"

    template_name = inscripciones_templates + "create.html"


    def get_form(self, form_class = None):

        form = super().get_form(form_class)
        form.fields["clase"].queryset = Clase.objects.filter(status__in=[Clase.Status.ACTIVO, Clase.Status.PAUSADO])
        form.fields["estudiante"].queryset = Estudiante.objects.filter(status=Estudiante.Status.ACTIVO)

        return form

    def get_success_url(self):
        return reverse("inscripciones-detail", kwargs={"pk":self.object.pk})


# Dia de Clases
dia_de_clase_templates = "gakusei/dia_de_clase/"

class DiaDeClaseListView(ListView):
    model = DiaDeClase
    ordering = "horario"

    template_name = dia_de_clase_templates + "list.html"


class DiaDeClaseDetailView(DetailView):
    model = DiaDeClase
    template_name = dia_de_clase_templates + "detail.html"


class DiaDeClaseCreateView(CreateView):
    model = DiaDeClase
    fields = "__all__"

    template_name = dia_de_clase_templates + "create.html"

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields["fecha"].widget = forms.DateInput(attrs={"type":"date"})

        return form

    def get_success_url(self):
        return reverse("dia-de-clase-detail", kwargs={"pk":self.object.pk})



# Asistencias
asistencia_templates = "gakusei/asistencia/"

class AsistenciaListView(ListView):
    model = Asistencias
    ordering = "dia_clase"

    template_name = asistencia_templates + "list.html"


class AsistenciaDetailView(DetailView):
    model = Asistencias
    template_name = asistencia_templates + "detail.html"


class AsistenciaCreateView(CreateView):
    model = Asistencias
    fields = "__all__"

    template_name = asistencia_templates + "create.html"

    def get_success_url(self):
        return reverse("asistencia-detail", kwargs={"pk":self.object.pk})


from django.forms import modelformset_factory
def AsistenciaCreate(request):
    
    clase_form = SeleccionAsistenciaForm()

    # Creamos el FormSet

    if request.method == "POST":
        # SOLO API

        clase = Clase.objects.get(pk=request.POST.get("clase"))
        estudiantes_numero = clase.inscripciones.count()    
        
        AsistenciaFormSet = modelformset_factory(Asistencias, form=AsistenciaForm, extra=estudiantes_numero, can_delete=False)
        formset = AsistenciaFormSet(request.POST)

        if formset.is_valid():
            print("yes")
            f = formset.save()
            print(f)
            return JsonResponse({"clase_id":request.POST.get("clase")}, status=200)

        return JsonResponse({"error_form":formset.as_div()}, status=400)
        

    else:
        formset = None


    return render(request, asistencia_templates+"create.html", {
        "clase_form":clase_form,
        "asistencia_form": formset,
    })


# API
def Api_RepresentantesGet(request):
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


def Api_ClaseGet(request):

    if request.method != "POST":
        return JsonResponse({"error": "Use method POST."}, status=403)
    

    body = loads(request.body)
    pk = body.get("pk", False)


    if not pk:
        return JsonResponse({"error":"Id no enviado"}, status=400)


    clase = Clase.objects.filter(pk=pk).first()

    if clase:
        return JsonResponse(model_to_dict(clase), status=201)
    
    return JsonResponse({"error": "Clase no encontrada"}, status=404)



def Api_EstudianteGet(request):

    if request.method != "POST":
        return JsonResponse({"error": "Use method POST."}, status=403)
    

    body = loads(request.body)
    pk = body.get("pk", False)


    if not pk:
        return JsonResponse({"error":"Id no enviado"}, status=400)


    try:
        estudiante = Estudiante.objects.filter(pk=pk).first()
    except Estudiante.DoesNotExist:
        return JsonResponse({"error": "Estudiante no encontrado"}, status=404)




    if _ := estudiante.beca():
        beca = model_to_dict(_)
    else:
        beca = False

    if _ := estudiante.descuento():
        descuento = model_to_dict(_)
    else:
        descuento = False


    submit = {
        "estudiante": model_to_dict(estudiante),
        "beca": beca,
        "descuento": descuento,
    }

    
    return JsonResponse(submit, status=201)
    
    


def Api_DiaDeClaseGet(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use method POST."}, status=403)
    

    body = loads(request.body)
    pk = body.get("pk", False)


    if not pk:
        return JsonResponse({"error":"Id no enviado"}, status=400)


    try:
        clase = Clase.objects.filter(pk=pk).first()
    except DiaDeClase.DoesNotExist:
        return JsonResponse({"error": "Clase no encontrado"}, status=404)
    

    # CONGER ID DE LOS HORARIOS Y LUEGOS HACER UN QUERY SEARCH PARA DIA DE CLASES.
    # POSIBLE PASAR FUNCION EN EL MISMO MODELO CLASE
    
    dias = DiaDeClase.objects.filter(horario__clase=clase)

    if not dias:
        return JsonResponse({"error": "No hay Dias de Clases registradas para esta clase."}, status=400)

    results = [
        {"id": d.pk, "text":str(d)}
        for d in dias
    ]

    return JsonResponse({"results":results}, status=201)
    



def Api_EstudiantesInscriptosGet(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use method POST."}, status=403)
    

    body = loads(request.body)
    clase_id = body.get("clase_id", False)
    dia_id = body.get("dia_id", False)


    if not clase_id or not dia_id:
        return JsonResponse({"error":"Id's no enviados"}, status=400)


    try:
        clase = Clase.objects.filter(pk=clase_id).first()
    except DiaDeClase.DoesNotExist:
        return JsonResponse({"error": "Clase no encontrado"}, status=404)
    

    estudiantes = Estudiante.objects.filter(inscripciones__clase=clase)

    estudiantes_data = []

    for e in estudiantes:
        estudiantes_data.append(dict(nombre_estudiante=str(e), estudiante=e.pk, dia_clase=dia_id))

# FALTA CORREGIR CUAL ES EL DIA DE LA CLASE
    estudiantes_numero = clase.inscripciones.count()

    AsistenciaFormSet = modelformset_factory(Asistencias, form=AsistenciaForm, extra=estudiantes_numero, can_delete=False)

    formset = AsistenciaFormSet(
        initial=estudiantes_data,
        queryset=Asistencias.objects.none(),
    )

    return JsonResponse({"form": formset.as_div()}, status=201)
    




def Api_EstudiantesInscriptosGetClasic(request):

    if request.method != "POST":
        return JsonResponse({"error": "Use method POST."}, status=403)
    

    body = loads(request.body)
    pk = body.get("pk", False)


    if not pk:
        return JsonResponse({"error":"Id no enviado"}, status=400)


    try:
        diadeclase = DiaDeClase.objects.filter(pk=pk).first()
    except DiaDeClase.DoesNotExist:
        return JsonResponse({"error": "Dia de Clase no encontrado"}, status=404)
    

    clase = diadeclase.horario.clase

    listado_de_inscripciones = Inscripciones.objects.filter(clase=clase)

    estudiantes_inscriptos = []

    if listado_de_inscripciones:
        for estudiante in listado_de_inscripciones:
            e = {
                "id": estudiante.estudiante.id,
                "text": estudiante.estudiante.__str__(),
            }

            estudiantes_inscriptos.append(e)

    submit = {
        "results": estudiantes_inscriptos,
    }

    return JsonResponse(submit, status=201)
    

    from django.forms.models import model_to_dict


