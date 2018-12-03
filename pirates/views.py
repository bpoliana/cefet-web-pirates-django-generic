from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField
from django.http import HttpResponseRedirect
from django.views import View
from django.forms import ModelForm
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Tesouro


class ListarTesouros(View):
    model = models.Tesouro
    template_name = 'lista_tesouros.html'

    def get_context_data(self, **kwargs)
        context = super().get_context_data(**kwargs)
                context['total_geral'] = 0
                for obj in context['object_list']:
                    context['total_geral'] += obj.valor_total
                return context

    def get_queryset(self, **kwargs):
        return models.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                            output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    )\
                              )


class TesouroForm(ModelForm):
    class Meta:
        model = Tesouro
        fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
        labels = {
            "img_tesouro": "Imagem"
        }

class SalvarTesouro(View):
    def get_tesouro(self,id):
        if id:
            return Tesouro.objects.get(id=id)
        return None

    def get(self,request,id=None):
        return render(request,"salvar_tesouro.html",{"tesouroForm":TesouroForm(instance=self.get_tesouro(id))})

    def post(self,request,id=None):
        form = TesouroForm(request.POST,request.FILES, instance=self.get_tesouro(id))

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('lista_tesouros') )
        else:
            return render(request,"salvar_tesouro.html",{"tesouroForm":form})

class RemoverTesouro(View):
    def get(self,request,id):
        Tesouro.objects.get(id=id).delete()
        return HttpResponseRedirect(reverse('lista_tesouros') )

class InserirTesouro(CreateView):
    class Meta:
        model = Tesouro
        fields = fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
        template_name = 'salvar_tesouro.html'
        success_url = reverse_lazy('lista_tesouros')
