from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .models import Sensei
from .forms import SenseiForm

from django.views.generic import ListView, DetailView, FormView, CreateView

# Create your views here.
def index(request):
    return render(request, "gakusei/index.html")


sensei_templates = "gakusei/sensei/"
def sensei(request):
    ...

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
    

    

    