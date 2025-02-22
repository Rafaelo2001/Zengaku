from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.db import transaction, IntegrityError
from json import loads

from django import forms
from django.forms import modelformset_factory
from django.forms.models import model_to_dict

from .models import Sensei, Estudiante, Representante, Clase, Horario, Inscripciones, DiaDeClase, Asistencias, Pagos, Sede, Curso, MetodosPagos, DescuentoEspecial, Becas, Becados
from .forms import SenseiForm, EstudianteForm, RepresentanteForm, SeleccionAsistenciaForm, AsistenciaForm, DiasForm, AsistenciaRezagadosForm

from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from dateutil.relativedelta import relativedelta


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


class SenseiCreateView(CreateView):
    model = Sensei
    form_class = SenseiForm
    template_name = sensei_templates + "create.html"

    def get_success_url(self):
        return reverse("sensei-detail", kwargs={"pk":self.object.pk})

    

class SenseiEditView(UpdateView):
    model = Sensei
    form_class = SenseiForm
    template_name = sensei_templates + "edit.html"

    def get_success_url(self):
        return reverse("sensei-detail", kwargs={"pk":self.object.pk})
    
    def get_form_kwargs(self):
        # Obtenemos los datos que seran colocados en los campos del formulario
        kwargs = super().get_form_kwargs()

        # Obtenemos al objeto que se va a Editar
        sensei = self.get_object()

        # Pegamos los datos de 'Personal Data' a la variable que será procesada en el __init__ del formulario
        kwargs["personal_data"] = {
            "nacionalidad"   : sensei.personal_data.nacionalidad,
            "cedula"         : sensei.personal_data.cedula,
            "first_name"     : sensei.personal_data.first_name,
            "middle_name"    : sensei.personal_data.middle_name,
            "last_name_1"    : sensei.personal_data.last_name_1,
            "last_name_2"    : sensei.personal_data.last_name_2,
            "telefono"       : sensei.personal_data.telefono,
            "personal_email" : sensei.personal_data.personal_email,
        }

        return kwargs

        
    

# Estudiante
estudiante_templates = "gakusei/estudiante/"
class EstudianteListView(ListView):
    model = Estudiante
    template_name = estudiante_templates + "list.html"


class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = estudiante_templates + "detail.html"


class EstudianteCreateView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = estudiante_templates + "create.html"

    def get_success_url(self):
        return reverse("estudiante-detail", kwargs={"pk":self.object.pk})


class EstudianteEditView(UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = estudiante_templates + "edit.html"

    def get_success_url(self):
        return reverse("estudiante-detail", kwargs={"pk":self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        estudiante = self.get_object()

        kwargs["personal_data"] = {
            "nacionalidad"   : estudiante.personal_data.nacionalidad,
            "cedula"         : estudiante.personal_data.cedula,
            "first_name"     : estudiante.personal_data.first_name,
            "middle_name"    : estudiante.personal_data.middle_name,
            "last_name_1"    : estudiante.personal_data.last_name_1,
            "last_name_2"    : estudiante.personal_data.last_name_2,
            "telefono"       : estudiante.personal_data.telefono,
            "personal_email" : estudiante.personal_data.personal_email,
        }

        return kwargs


    
    
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


class ClaseEditView(UpdateView):
    model = Clase
    fields = "__all__"
    template_name = clase_templates + "edit.html"

    def get_success_url(self):
        return reverse("clase-detail", kwargs={"pk": self.object.pk})

    def get_form(self, form_class = None):

        form = super().get_form(form_class)

        form.fields["f_inicio"].widget = forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")
        form.fields["f_cierre"].widget = forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")

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

        if clase_id := self.request.GET.get("clase"):
            readonly_select = {"onfocus":"this.blur();", "style":"pointer-events: none;", "disabled":"true"}
            form.fields["clase"].widget.attrs.update(readonly_select)

        return form
    
    def get_initial(self):
        initial = super().get_initial()

        clase_id = self.request.GET.get("clase")

        if clase_id:
            initial["clase"] = clase_id

        return initial




class HorarioEditView(UpdateView):
    model = Horario
    fields = "__all__"
    template_name = horario_templates + "edit.html"

    def get_success_url(self):
        return reverse("horario-detail", kwargs={"pk": self.object.pk})

    def get_form(self, form_class = None):

        form = super().get_form(form_class)

        form.fields["hora_entrada"].widget = forms.TimeInput(attrs={"type":"time", "step":"1"})
        form.fields["hora_salida"].widget  = forms.TimeInput(attrs={"type":"time", "step":"1"})

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

    def get_initial(self):
        initial = super().get_initial()

        if clase_id := self.request.GET.get("clase"):
            initial["clase"] = clase_id

        if estudiante_id := self.request.GET.get("estudiante"):
            initial["estudiante"] = estudiante_id

        return initial


    def get_form(self, form_class = None):

        form = super().get_form(form_class)
        form.fields["clase"].queryset = Clase.objects.filter(status__in=[Clase.Status.ACTIVO, Clase.Status.PAUSADO])
        form.fields["estudiante"].queryset = Estudiante.objects.filter(status=Estudiante.Status.ACTIVO)

        readonly_select = {"onfocus":"this.blur();", "style":"pointer-events: none;", "disabled":"true"}

        if clase_id := self.request.GET.get("clase"):

            form.fields["estudiante"].queryset = Estudiante.objects.filter(
                status=Estudiante.Status.ACTIVO
            ).exclude(
                pk__in=Inscripciones.objects.filter(clase=Clase.objects.filter(pk=clase_id)[0]).values_list("estudiante", flat=True)
            )

            form.fields["clase"].widget.attrs.update(readonly_select)

        if estudiante_id := self.request.GET.get("estudiante"):
            form.fields["estudiante"].widget.attrs.update(readonly_select)

        return form

    def get_success_url(self):
        return reverse("inscripciones-detail", kwargs={"pk":self.object.pk})


class InscripcionesEditView(UpdateView):
    model = Inscripciones
    fields = "__all__"

    template_name = inscripciones_templates + "edit.html"


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
    ordering = "-fecha"

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_clase"] = SeleccionAsistenciaForm()

        return context

    def get_success_url(self):
        return reverse("dia-de-clase-detail", kwargs={"pk":self.object.pk})
    

class DiaDeClaseEditView(UpdateView):
    model = DiaDeClase
    fields = "__all__"

    template_name = dia_de_clase_templates + "edit.html"

    def get_form(self, form_class = None):
        form = super().get_form(form_class)

        print(self.object.clase())
        
        form.fields["horario"].queryset = Horario.objects.filter(clase=self.object.clase())
        form.fields["fecha"].widget = forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")

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



def AsistenciaCreate(request):

    if request.method == "POST":
        try:
            with transaction.atomic():

                clase = get_object_or_404(klass=Clase, pk=request.POST.get("clase"))
                estudiantes_numero = clase.inscripciones.count()    

                dias_form = DiasForm(request.POST)

                if dias_form.is_valid():
                    dia = dias_form.save()

                    # Como no se puede alterar el formset despues de creado y el request no puede ser modificado,
                    # creamos una copia y agregamos el dia_clase ahi
                    post_data = request.POST.copy()

                    for _ in range(int(post_data["form-TOTAL_FORMS"])):
                        post_data[f"form-{_}-dia_clase"] = dia

                    AsistenciaFormSet = modelformset_factory(Asistencias, form=AsistenciaForm, extra=estudiantes_numero, can_delete=False)
                    formset = AsistenciaFormSet(post_data)


                    if formset.is_valid():
                        formset.save()

                        response = {
                            "url_redirect": reverse("dia-de-clase-detail", kwargs={"pk":dia.pk}),
                        }

                        return JsonResponse(response, status=200)
                    else:
                        print(formset.errors)
                        raise Exception("Formset no valid")
                    
                else:
                    raise Exception("Dias no valid")
        
        except Exception as e:
            return JsonResponse({"error": f"Error al insertar datos en BDD: {e}"}, status=400)



    return render(request, asistencia_templates + "create.html", {
        "clase_form": SeleccionAsistenciaForm()
    })



class AsistenciaCreateViewClasic(CreateView):
    # ASISTENCIAS-CLASIC
    model = Asistencias
    fields = "__all__"

    template_name = asistencia_templates + "create-all-at-once.html"

    def get_success_url(self):
        return reverse("asistencia-detail", kwargs={"pk":self.object.pk})



def AsistenciaCreateRezagados(request):

    if request.method == "POST":
        # SOLO API
        clase = Clase.objects.get(pk=request.POST.get("clase"))

        form = AsistenciaRezagadosForm(request.POST)

        if form.is_valid():
            
            f = form.save()
            dia = f.dia_clase

            return JsonResponse({"url_redirect":reverse("dia-de-clase-detail", kwargs={"pk":dia.pk})}, status=200)
        
        else:
            form.fields["dia_clase"].queryset = DiaDeClase.objects.filter(horario__clase=clase)

        return JsonResponse({"error_form":form.as_div()}, status=400)

    # if "clase" in request.GET:
    #     # Acomodar esto despues para cada clase
    #     print("GET", request.GET)
    #     clase_form = SeleccionAsistenciaForm()
    #     clase_form.fields["clase"].widget = forms.TextInput()
    #     clase_form.fields["clase"].initial = "2"

    else:
        clase_form = SeleccionAsistenciaForm()

    return render(request, asistencia_templates + "create-rezagados.html", {
        "clase_form": clase_form,
    })


class AsistenciaEditView(UpdateView):
    model = Asistencias
    template_name = asistencia_templates + "edit.html"
    fields = "__all__"

    def get_form(self, form_class = None):
        form = super().get_form(form_class)

        readonly_select = {"onfocus":"this.blur();", "style":"pointer-events: none;", "disabled":"true"}
        
        form.fields["dia_clase"].widget.attrs.update(readonly_select)
        form.fields["estudiante"].widget.attrs.update(readonly_select)

        return form


    def get_success_url(self):
        return reverse("dia-de-clase-detail", kwargs={"pk":self.object.dia_clase.pk})


# PAGOS
pagos_templates = "gakusei/pagos/"

class PagosListView(ListView):
    model = Pagos
    ordering = "-fecha"

    template_name = pagos_templates + "list.html"


class PagosDetailView(DetailView):
    model = Pagos
    template_name = pagos_templates + "detail.html"



class PagosCreateView(CreateView):
    model = Pagos
    fields = "__all__"

    template_name = pagos_templates + "create.html"
    
    
    def get_success_url(self):
        return reverse("pagos-detail", kwargs={"pk":self.object.pk})




# SOLVENCIAS
solvencias_templates = "gakusei/solvencia/"
 
class SolvenciaClaseListView(ListView):
    model = Clase
    template_name = solvencias_templates + "list-clase.html"


class SolvenciaClaseDetailView(DetailView):
    model = Clase
    template_name = solvencias_templates + "detail-clase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # f_inicio = context["clase"].f_inicio
        # from datetime import date, datetime;

        # print(f_inicio)
        # print(date.today())

        # diferencia = relativedelta(date.today(), f_inicio)

        # print(diferencia)
        
        return context



# Sedes
sede_templates = "gakusei/sede/"

class SedeListView(ListView):
    model = Sede
    template_name = sede_templates + "list.html"


class SedeDetailView(DetailView):
    model = Sede
    template_name = sede_templates + "detail.html"


class SedeCreateView(CreateView):
    model = Sede
    fields = "__all__"

    template_name = sede_templates + "create.html"

    def get_success_url(self):
        return reverse("sede-detail", kwargs={"pk":self.object.pk})



# Curso
curso_templates = "gakusei/curso/"

class CursoListView(ListView):
    model = Curso
    template_name = curso_templates + "list.html"


class CursoDetailView(DetailView):
    model = Curso
    template_name = curso_templates + "detail.html"


class CursoCreateView(CreateView):
    model = Curso
    fields = "__all__"

    template_name = curso_templates + "create.html"

    def get_success_url(self):
        return reverse("curso-detail", kwargs={"pk":self.object.pk})
    




# Métodos de Pago
metodo_templates = "gakusei/metodos_pago/"

class MetodosPagoListView(ListView):
    model = MetodosPagos
    template_name = metodo_templates + "list.html"


class MetodosPagoDetailView(DetailView):
    model = MetodosPagos
    template_name = metodo_templates + "detail.html"


class MetodosPagoCreateView(CreateView):
    model = MetodosPagos
    fields = "__all__"

    template_name = metodo_templates + "create.html"

    def get_success_url(self):
        return reverse("metodos-pago-detail", kwargs={"pk":self.object.pk})





# Descuentos Especiales
descuento_templates = "gakusei/descuentos_especiales/"

class DescuentoEspecialListView(ListView):
    model = DescuentoEspecial
    template_name = descuento_templates + "list.html"


class DescuentoEspecialDetailView(DetailView):
    model = DescuentoEspecial
    template_name = descuento_templates + "detail.html"


class DescuentoEspecialCreateView(CreateView):
    model = DescuentoEspecial
    fields = "__all__"

    template_name = descuento_templates + "create.html"

    def get_success_url(self):
        return reverse("descuento-especial-detail", kwargs={"pk":self.object.pk})





# Becas
becas_templates = "gakusei/beca/"

class BecaListView(ListView):
    model = Becas
    template_name = becas_templates + "list.html"


class BecaDetailView(DetailView):
    model = Becas
    template_name = becas_templates + "detail.html"


class BecaCreateView(CreateView):
    model = Becas
    fields = "__all__"

    template_name = becas_templates + "create.html"

    def get_success_url(self):
        return reverse("becas-detail", kwargs={"pk":self.object.pk})
    

class BecaAssingView(CreateView):
    model = Becados
    fields = "__all__"

    template_name = becas_templates + "asignar.html"

    def get_success_url(self):
        return reverse("becas-detail", kwargs={"pk":self.object.pk})





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



def Api_AsistenciaForm(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use method POST."}, status=403)
    

    body = loads(request.body)
    clase_id = body.get("pk", False)


    if not clase_id:
        return JsonResponse({"error":"Id no enviados"}, status=400)


    try:
        clase = Clase.objects.filter(pk=clase_id).first()
    except DiaDeClase.DoesNotExist:
        return JsonResponse({"error": "Clase no encontrado"}, status=404)
    

    estudiantes = Estudiante.objects.filter(inscripciones__clase=clase)

    estudiantes_data = []

    for e in estudiantes:
        estudiantes_data.append(dict(nombre_estudiante=str(e), estudiante=e.pk))

    estudiantes_numero = clase.inscripciones.count()

    AsistenciaFormSet = modelformset_factory(Asistencias, form=AsistenciaForm, extra=estudiantes_numero, can_delete=False)

    formset = AsistenciaFormSet(
        initial=estudiantes_data,
        queryset=Asistencias.objects.none(),
    )

    dia_form = DiasForm()

    dia_form.fields["horario"].queryset = Horario.objects.filter(clase=clase).order_by("dia_semana")

    response = {
        "dias_form": dia_form.as_div(),
        "formset": formset.as_div()
    }

    return JsonResponse(response, status=201)



def Api_AsistenciaFormRezagados(request):
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
    
    
    dias = DiaDeClase.objects.filter(horario__clase=clase)

    if not dias:
        return JsonResponse({"error": "No hay Dias de Clases registradas para esta clase."}, status=400)
    

    estudiantes = Estudiante.objects.filter(inscripciones__clase=clase)

    form = AsistenciaRezagadosForm()

    form.fields["dia_clase"].queryset = dias
    form.fields["estudiante"].queryset = estudiantes


    return JsonResponse({"form":form.as_div()}, status=201)
    


# Obtiene las Clases a las cuales esta inscripto un estudiante.
def Api_Pagos_Clases(request):

    if request.method != "POST":
        return JsonResponse({"error": "Use method POST."}, status=403)
    

    body = loads(request.body)
    pk = body.get("pk", False)


    if not pk:
        return JsonResponse({"error":"Id no enviado"}, status=400)


    try:
        estudiante = Estudiante.objects.filter(pk=pk).first()
    except DiaDeClase.DoesNotExist:
        return JsonResponse({"error": "Estudiante no encontrado"}, status=404)
    

    clases = Clase.objects.filter(inscripciones__estudiante=estudiante)

    if clases:

        results = [
            {"id": c.id, "text": str(c)}
            for c in clases
        ]

        return JsonResponse({"results":results}, status=200)
    
    else:
        return JsonResponse({"error": "Estudiante no esta registrado en ninguna clase."}, status=404)


# Obtiene la mensualidad dado un estudiante y la clase
def Api_Pagos_Mensualidad(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "Use method POST."}, status=403)
    

    body = loads(request.body)
    id_estudiante = body.get("estudiante", False)
    id_clase = body.get("clase", False)


    if not id_estudiante or not id_clase:
        return JsonResponse({"error":"Ids no enviados"}, status=400)
    

    try:
        inscripcion = Inscripciones.objects.filter(estudiante=id_estudiante, clase=id_clase).first()
    except Inscripciones.DoesNotExist:
        return JsonResponse({"error": "Inscripcion no encontrada"}, status=404)

    return JsonResponse({"mensualidad":inscripcion.precio_a_pagar}, status=200)




def Api_DiasDeClase_Form(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use method POST."}, status=403)
    

    body = loads(request.body)
    clase_id = body.get("pk", False)


    if not clase_id:
        return JsonResponse({"error":"Id no enviado"}, status=400)


    try:
        clase = Clase.objects.filter(pk=clase_id).first()
    except Clase.DoesNotExist:
        return JsonResponse({"error": "Clase no encontrado"}, status=404)
    

    dia_form = DiasForm()
    dia_form.fields["horario"].queryset = Horario.objects.filter(clase=clase).order_by("dia_semana")


    return JsonResponse({"dias_form": dia_form.as_div()}, status=201)
