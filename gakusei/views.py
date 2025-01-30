from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from json import loads

from .models import Sensei, Estudiante
from .forms import SenseiForm, EstudianteForm

from django.views.generic import ListView, DetailView, FormView

# Create your views here.
def index(request):
    return render(request, "gakusei/index.html")


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
    

estudiante_templates = "gakusei/estudiantes/"
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
    

# def Api_RespresentanteRegistro(request):

#     if request.method == "POST":
#         representante = RepresentanteForm(loads(request.body))

#         print(representante.is_valid())
        
#         if representante.is_valid():
#             r = representante.save()

#             response = {
#                 "id": r.pk,
#                 "str": r.__str__(),
#             }

#             return JsonResponse(response, status=201)
        
#         return JsonResponse({"error_form": representante.as_div()}, status=422)

#     return JsonResponse({"a":"o"})

# def Api_RepresentanteEdit(request):
#     if request.method == "POST":
#         response = loads(request.body)
        
#         representante = Representante.objects.get(pk=response.get('id'))

#         edit_form = RepresentanteForm()
#         edit_form.unpack(repre_obj=representante)

#         return JsonResponse({"edit_form": edit_form.as_div()})
    
#     elif request.method == "PUT":
#         data = loads(request.body)

#         edited = RepresentanteForm(data)

#         if edited.is_valid():
#             response = edited.update(id=data.get('id'))

#             response = {
#                 "id": r.pk,
#                 "str": r.__str__(),
#             }

#             return JsonResponse(response, status=201)
        
#         return JsonResponse({"error_form": edited.as_div()}, status=422)

