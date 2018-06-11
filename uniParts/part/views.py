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
    global parte
    if request.user.is_anonymous:
        pass
    else:
        setorP = SetorParte.objects.filter(setor=request.user.profile.setor)
    if request.user.is_superuser:
        if query:
            if tipo == "publicadas":
                parte = Parte.objects.filter(descricao__icontains=query, status__icontains='PUBLICADO')
            elif tipo == "outros":
                if not setorP:
                    pass
                else:
                   for p in setorP:
                       parte = Parte.objects.filter(pk=p.parte.pk,descricao__icontains=query,boletim_interno=None).exclude(
                        status__icontains='PUBLICADO')
            elif tipo != "todas":
                parte = Parte.objects.filter(descricao__icontains=query, tipoParte__tpDescricao__icontains=tipo)
            else:
                parte = Parte.objects.filter(descricao__icontains=query)
        else:
            if tipo == "publicadas":
                parte = Parte.objects.filter(status__icontains='PUBLICADO')
            elif tipo == "outros":
                if not setorP:
                    pass
                else:
                   for p in setorP:
                       parte = Parte.objects.filter(pk=p.parte.pk,boletim_interno=None).exclude(
                        status__icontains='PUBLICADO')
            elif tipo != "todas":
                parte = Parte.objects.filter(tipoParte__tpDescricao__icontains=tipo).exclude(
                    status__icontains='PUBLICADO')
            else:
                parte = Parte.objects.all()
    else:
        if query:
            if tipo == "publicadas":
                parte = Parte.objects.filter(author=request.user, descricao__icontains=query, status__icontains='PUBLICADO')
            elif tipo == "outros":
                if not setorP:
                    pass
                else:
                    for p in setorP:
                        parte = Parte.objects.filter(pk=p.parte.pk,descricao__icontains=query,boletim_interno=None).exclude(
                        status__icontains='PUBLICADO')
            elif tipo != "todas":
                parte = Parte.objects.filter(author=request.user, descricao__icontains=query, tipoParte__tpDescricao__icontains=tipo)
            else:
                parte = Parte.objects.filter(author=request.user, descricao__icontains=query)
        else:
            if tipo == "publicadas":
                parte = Parte.objects.filter(author=request.user, status__contains='PUBLICADO')
            elif tipo == "outros":
                if not setorP:
                    pass
                else:
                    for p in setorP:
                        parte = Parte.objects.filter(pk=p.parte.pk,boletim_interno=None).exclude(
                        status__icontains='PUBLICADO')
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
    alerta = total_alertas_nao_lidos()
    validacao = Validacao.objects.select_related('parte')
    setor = SetorParte.objects.select_related('parte')
    contexto = {'lista': parte, 'validations': validacao, 'setores' : setor, 'alerta' : alerta}
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
                ale.descricao = 'Novo atestado de ' + usuario.get_full_name()
                ale.data_alerta = timezone.now()
                ale.save()
            encaminhar_parte_novo(parte.pk)
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
    response['Content-Disposition'] = 'attachment; filename="parte_'+str(par.id)+'.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    p.setFont('Courier', 12)
    # Cabeçalho lado esquerdo
    local = par.author.profile.setor
    p.drawString(20, 800, 'PMPR')
    p.drawString(20, 785, '5º CRPM')
    p.drawString(20, 770, '6º BPM')
    p.drawString(20, 755, str(local))
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
    nombre.append('Do '+par.author.profile.graduacao)
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
    p.drawString(20,y-30, 'No período de '+dia_inicio+' '+Meses[mes_inicio]+' '+ano_inicio+ ' até o dia '+dia_fim+' '+Meses[mes_fim]+' '+ano_fim+'.')
    # Nome do solicitante
    yyy = 240
    for l in wrap(nombre, 40):
        p.drawString(300, yyy, l)
        yyy -=15
    p.setFont('Courier-Bold', 12)
    profile = Profile.objects.get(user=par.author)
    p.drawString(355,yyy, 'Solicitante')
    p.drawString(350,yyy-15, 'RG: ' + profile.rg)
    p.showPage()
    validacoes = Validacao.objects.select_related('parte').order_by('data_autorizacao')
    yyyy = 650
    zzz = 30
    qtd = 0
    for v in validacoes:
        if v.parte == par:
            qtd += 1
            p.setFont('Courier', 12)
            # Cabeçalho lado esquerdo
            p.drawString(zzz, yyyy+150, 'PMPR')
            p.drawString(zzz, yyyy+135, '5º CRPM')
            p.drawString(zzz, yyyy+120, '6º BPM')

            dia_v = v.data_autorizacao.strftime('%d')
            mes_v = v.data_autorizacao.month - 1
            ano_v = v.data_autorizacao.strftime('%Y')
            p.drawString(zzz, yyyy+15,'Ciente em: '+ dia_v + ' ' + Meses[mes_v] + ' ' + ano_v)

            for line in wrap(v.observacao, 30):
                p.drawString(zzz, yyyy, line)
                yyyy -= 15

            if v.user_validacao != None:
                yyyy -= 45
                p.drawString(zzz,yyyy,v.user_validacao.profile.graduacao+' '+v.user_validacao.get_full_name())
            yyyy -= 200

            if qtd == 2:
                zzz += 300
                yyyy = 650
            if qtd == 4:
                p.showPage()
                yyyy = 650
                zzz = 30
                qtd = 0
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

def encaminhar_parte(request, pk):
    par = get_object_or_404(Parte, pk=pk)
    if request.method == "POST":
        form = SetorParteForm(request.POST, pk)
        if form.is_valid():
            sp = form.save(commit=False)
            setorP = SetorParte.objects.filter(parte=par)
            usuario = request.user
            profile = Profile.objects.get(user=usuario)
            if not setorP:
                sp.parte = par
                sp.setor = form.cleaned_data['setor']
                sp.data_enc = timezone.now()
                sp.observacao = 'Encaminhado ao setor ' + sp.setor.__str__() + ' Por: '+ profile.graduacao + ' ' + usuario.get_full_name()
                sp.save()
            else:
                for setorParte in setorP:
                    setorParte.setor = form.cleaned_data['setor']
                    setorParte.data_enc = timezone.now()
                    setorParte.observacao = 'Encaminhado ao setor '+ setorParte.setor.__str__() + ' Por: '+ profile.graduacao + ' ' + usuario.get_full_name()
                    setorParte.save()
            return redirect('/partes/listar/todas/')
    else:
        form = SetorParteForm()
    return render(request, 'validacao_edit.html', {'form': form})

def encaminhar_parte_novo(pk):
    par = get_object_or_404(Parte, pk=pk)
    profile = Profile.objects.get(user=par.author)
    sp = SetorParte()
    sp.parte = par
    sp.setor = profile.setor
    sp.data_enc = timezone.now()
    sp.observacao = 'Encaminhado ao setor ' + sp.setor.__str__() + ' Por: '+ profile.graduacao + ' ' + par.author.get_full_name()
    sp.save()

def total_alertas_nao_lidos():
    atestados = Alerta.objects.filter().exclude(lido=True)
    return atestados

def alerta_lido(request, pk):
    alerta = get_object_or_404(Alerta, pk=pk)
    alerta.lido = True
    alerta.save()
    return redirect('/partes/listar/todas/')