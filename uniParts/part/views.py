from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import redirect
from .forms import *

def parts_list(request, tipo, template_name="parts_list.html"):
    usuario = request.user
    query = request.GET.get("busca", '')
    if usuario.is_superuser:
            if query:
                if tipo == "publicadas":
                     parte = Parte.objects.filter(descricao__icontains=query, status__icontains='PUBLICADO')
                elif tipo != "todas":
                     parte = Parte.objects.filter(descricao__icontains=query, tipoParte__tpDescricao__icontains=tipo)
                else:
                     parte = Parte.objects.filter(descricao__icontains=query)
            else:
                 if tipo == "publicadas":
                    parte = Parte.objects.filter(status__icontains='PUBLICADO')
                 elif tipo != "todas":
                    parte = Parte.objects.filter(tipoParte__tpDescricao__icontains=tipo)
                 else:
                    parte = Parte.objects.all()
    else:
            if query:
                if tipo == "publicadas":
                    parte = Parte.objects.filter(descricao__icontains=query, status__icontains='PUBLICADO')
                elif tipo != "todas":
                    parte = Parte.objects.filter(author=usuario,descricao__icontains=query, tipoParte__tpDescricao__icontains=tipo)
                else:
                    parte = Parte.objects.filter(author=usuario,descricao__icontains=query)
            else:
                if tipo == "publicadas":
                    parte = Parte.objects.filter(author=usuario,status__contains='PUBLICADO')
                elif tipo != "todas":
                    parte = Parte.objects.filter(author=usuario,tipoParte__tpDescricao__icontains=tipo)
                else:
                    parte = Parte.objects.filter(author=usuario)
    validacao = Validacao.objects.select_related('parte')
    contexto = {'lista':parte, 'validations':validacao}
    return render(request,template_name,contexto)

def parte_new(request):
    if request.method == "POST":
        form = ParteForm(request.POST)
        if form.is_valid():
            usuario = request.user
            parte = form.save(commit=False)
            parte.author = request.user
            parte.status = 'NOVA'
            parte.data_criacao = timezone.now()
            parte.save()
            if 'Atestado' in parte.tipoParte.tpDescricao:
                ale = Alerta()
                ale.descricao = 'Novo atestado do ' + usuario.first_name
                ale.data_alerta = timezone.now()
                ale.save()

            return redirect('/admin/part/parte/', pk=parte.pk)
    else:
        form = ParteForm()
    return render(request, 'parts_edit.html', {'form': form})

def parte_edit(request, pk):
    parte = get_object_or_404(Parte, pk=pk)
    if request.method == "POST":
        form = ParteForm(request.POST, instance=parte)
        if form.is_valid():
            parte = form.save(commit=False)
            parte.author = request.user
            parte.data_criacao = timezone.now()
            parte.save()
            return redirect('parts_detail', pk=parte.pk)
    else:
        form = ParteForm(instance=parte)
        return render(request, 'parts_edit.html', {'form': form})

def validacao_new(request, pk):
    par = get_object_or_404(Parte, pk=pk)
    if request.method == "POST":
        form = ValidacaoForm(request.POST, pk)
        if form.is_valid():
            validacao = form.save(commit=False)
            validacao.parte = par
            validacao.data_autorizacao = timezone.now()
            validacao.save()
            validacoes = Validacao.objects.select_related('parte')
            i = 0
            for v in validacoes:
                if v.parte == par:
                    i = i + 1
            print(i)
            print(par.tipoParte.qtd_validacoes)
            if i >= par.tipoParte.qtd_validacoes:
                par.status = 'AUTORIZADO'
                print(par.status)
                par.save()
            else:
                par.status = 'EM_ANALISE'
                print(par.status)
                par.save()
        return redirect('/admin/part/validacao/', pk=validacao.pk)
    else:
        form = ValidacaoForm()
    return render(request, 'validacao_edit.html', {'form': form})