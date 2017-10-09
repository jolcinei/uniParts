from textwrap import wrap
from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import redirect
from .forms import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse


def parts_list(request, tipo=None, template_name="parts_list.html"):
    if tipo == None:
        tipo = "todas"
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
            usuario = request.user
            validacao.observacao = validacao.observacao + ' Por: '+ usuario.first_name
            validacao.user_validacao = usuario
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
    Meses = ('Jan', 'Fev.', 'Mar.', 'Abr.', 'Maio', 'Jun.',
    'Jul.', 'Ago.', 'Set.', 'Out.', 'Nov.', 'Dez.')
    dia = par.data_criacao.strftime('%d')
    mes = par.data_criacao.month-1
    ano = par.data_criacao.strftime('%Y')
    #data = par.data_criacao.strftime('%d/%m/%Y')
    yy = 770
    xx = 370
    p.drawString(xx, 800, 'Cascavel ' + dia + ' ' + Meses[mes] + ' ' + ano)
    numero = format(par.id)
    p.drawString(xx, 785, 'Parte nº ' + numero)
    nome = str(par.author.get_full_name())
    nombre = []
    nombre.append('Do Sd. QPM 1-0 ')
    nombre.append(nome)
    nombre = ''.join(nombre)
    for n in wrap(nombre,25):
        p.drawString(xx, yy,  n.title())
        yy -=15
    p.drawString(xx, yy, 'Assunto: '+str(par.tipoParte))
    # Texto da parte
    y = 550
    for line in wrap(par.descricao, 75):
        p.drawString(20, y, line)
        y -= 15
    dia_inicio = par.data_inicio.strftime('%d')
    mes_inicio = par.data_inicio.month-1
    ano_inicio = par.data_inicio.strftime('%Y')
    dia_fim = par.data_fim.strftime('%d')
    mes_fim = par.data_fim.month - 1
    ano_fim = par.data_fim.strftime('%Y')
    p.drawString(20,y, 'No período de '+dia_inicio+' '+Meses[mes_inicio]+' '+ano_inicio+ ' até o dia '+dia_fim+' '+Meses[mes_fim]+' '+ano_fim+'.')
    # Nome do solicitante
    yyy = 240
    for l in wrap(nombre, 40):
        p.drawString(300, yyy, l)
        yyy -=15
    p.setFont('Courier-Bold', 12)
    p.drawString(350, yyy, 'Solicitante')
    p.showPage()
    validacoes = Validacao.objects.select_related('parte')
    yyyy = 650
    for v in validacoes:
        if v.parte == par:
            p.setFont('Courier', 12)
            # Cabeçalho lado esquerdo
            p.drawString(20, 800, 'PMPR')
            p.drawString(20, 785, '5º CRPM')
            p.drawString(20, 770, '6º BPM')


            for line in wrap(v.observacao, 30):
                p.drawString(20, yyyy, line)
                yyyy -= 15

            if v.user_validacao != None:
                p.drawString(45,yyyy-45,v.user_validacao.get_full_name())
            p.showPage()
    p.save()
    return response

def negado(request, pk):
    parte = get_object_or_404(Parte, pk=pk)
    parte.status = 'NEGADO'
    usuario = request.user
    validacao = Validacao()
    validacao.observacao = 'Negado por ' + usuario.first_name + ' em pré analise.'
    validacao.data_autorizacao = timezone.now()
    validacao.user_validacao = usuario
    validacao.parte = parte
    validacao.save()
    parte.save()
    return redirect('/partes/listar/todas/')
