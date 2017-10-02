from textwrap import wrap

from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import redirect
from .forms import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.http import HttpResponse


def parts_list(request, tipo, template_name="parts_list.html"):
    query = request.GET.get("busca", '')
    if request.user.is_superuser:
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
                parte = Parte.objects.filter(tipoParte__tpDescricao__icontains=tipo).exclude(
                    status__icontains='PUBLICADO')
            else:
                parte = Parte.objects.all()
    else:
        if query:
            if tipo == "publicadas":
                parte = Parte.objects.filter(descricao__icontains=query, status__icontains='PUBLICADO')
            elif tipo != "todas":
                parte = Parte.objects.filter(author=request.user, descricao__icontains=query,
                                             tipoParte__tpDescricao__icontains=tipo)
            else:
                parte = Parte.objects.filter(author=request.user, descricao__icontains=query)
        else:
            if tipo == "publicadas":
                parte = Parte.objects.filter(author=request.user, status__contains='PUBLICADO')
            elif tipo != "todas":
                if request.user.is_anonymous:
                    parte = Parte.objects.filter(tipoParte__tpDescricao__icontains=tipo)
                else:
                    parte = Parte.objects.filter(author=request.user, tipoParte__tpDescricao__icontains=tipo).exclude(
                        status__icontains='PUBLICADO')
            else:
                if request.user.is_anonymous:
                    parte = Parte.objects.all()
                else:
                    parte = Parte.objects.filter(author=request.user)
    validacao = Validacao.objects.select_related('parte')
    contexto = {'lista': parte, 'validations': validacao}
    return render(request, template_name, contexto)


def parte_new(request):
    if request.method == "POST":
        form = ParteForm(request.POST, request.FILES)
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
            return redirect('/partes/listar/todas/')
    else:
        form = ParteForm()
    return render(request, 'parts_edit.html', {'form': form})


def parte_edit(request, pk):
    parte = get_object_or_404(Parte, pk=pk)
    if request.method == "POST":
        form = ParteValidacaoForm(request.POST, instance=parte)
        if form.is_valid():
            parte = form.save(commit=False)
            parte.status = 'PUBLICADO'
            parte.save()
            return redirect('/partes/listar/todas/')
    else:
        form = ParteValidacaoForm(instance=parte)
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
            return redirect('/partes/listar/todas/')
    else:
        form = ValidacaoForm()
    return render(request, 'validacao_edit.html', {'form': form})


def exportToPdf(request, pk):
    par = get_object_or_404(Parte, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="partes.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    p.setFont('Courier', 12)
    # Cabeçalho lado esquerdo
    p.drawString(20, 800, 'PMPR')
    p.drawString(20, 785, '5º CRPM')
    p.drawString(20, 770, '6º BPM')
    # Cabeçalho lado direito
    data = format(par.data_criacao)
    p.drawString(360, 800, 'Cascavel ' + data)
    numero = format(par.id)
    p.drawString(360, 785, 'Parte nº ' + numero)
    nome = format(par.author.get_full_name())
    p.drawString(360, 770, 'Do Sd. QPM 1-0 ' + nome.title())
    p.drawString(360, 755, 'Assunto: '+str(par.tipoParte))
    # Texto da parte
    y = 550
    for line in wrap(par.descricao, 70):
        p.drawString(20, y, line)
        y -= 15

    # Nome do solicitante
    p.drawString(300, 240, 'Sd. QPM 1-0 ' + nome.title())
    p.showPage()
    p.save()
    return response
