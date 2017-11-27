from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
# Create your models here.
class Alerta(models.Model):
    descricao = models.CharField(null=False,max_length=200)
    data_alerta = models.DateField(verbose_name='Data')
    lido = models.NullBooleanField(null=True,blank=True)

    def __str__(self):
        return self.descricao

class TipoParte(models.Model):
    tpDescricao = models.CharField(verbose_name='Descrição',null=False,max_length=200)
    tpModelo = models.TextField(verbose_name='Modelo',null=False)
    alerta = models.ForeignKey(Alerta,null=True,blank=True)
    qtd_validacoes = models.IntegerField(verbose_name='Quantidade Validações',null=False)
    def hasAlert(self):
        self.alerta.lido = True

    def __str__(self):
        return self.tpDescricao

    def __unicode__(self):
        return self.tpDescricao

class NivelAutorizacao(models.Model):
    SUP='superior'
    SUB='subcomando'
    COM='comando'
    NEM='nenhum'
    NIVEL = (
        (SUP, 'SUPERIOR'),
        (SUB, 'SUBCOMANDO'),
        (COM, 'COMANDO'),
        (NEM, 'NENHUM')
    )
    nivel = models.CharField(max_length=20,choices=NIVEL)
    def __str__(self):
        return str(self.nivel)

    def __unicode__(self):
        return self.nivel

class Setor(models.Model):
    P1= 'P1'
    P2= 'P2'
    P3= 'P3'
    P4= 'P4'
    P5= 'P5'
    CMD='Cmd'
    SUBCMD = 'SubCmd'
    ALMOX = 'Almoxarifado'
    PRIMEIRA_CIA = '1ª Cia'
    SEGUNDA_CIA = '2ª Cia'
    TERCEIRA_CIA = '3ª Cia'
    QUARTA_CIA = '4ª Cia'
    SETOR = (
        (P1 , 'P1'),
        (P2 , 'P2'),
        (P3 , 'P3'),
        (P4 , 'P4'),
        (P5 , 'P5'),
        (CMD , 'Cmd'),
        (SUBCMD, 'SubCmd'),
        (ALMOX , 'Almoxarifado'),
        (PRIMEIRA_CIA , '1ª Cia'),
        (SEGUNDA_CIA , '2ª Cia'),
        (TERCEIRA_CIA , '3ª Cia'),
        (QUARTA_CIA , '4ª Cia'),
    )
    setor = models.CharField(max_length=32,choices=SETOR)
    def __str__(self):
        return str(self.setor)

    def __unicode__(self):
        return self.setor

class Parte(models.Model):
    NOVA = 'NOVA'
    AUTORIZADO = 'AUTORIZADO'
    EM_ANALISE = 'EM_ANALISE'
    NEGADO = 'NEGADO'
    PUBLICADO = 'PUBLICADO'
    STATUS = (
        (NOVA, 'NOVA'),
        (AUTORIZADO, 'AUTORIZADO'),
        (EM_ANALISE, 'EM ANALISE'),
        (NEGADO, 'NEGADO'),
        (PUBLICADO, 'PUBLICADO'),
    )
    status = models.CharField(max_length=32,choices=STATUS)
    author = models.ForeignKey('auth.User')
    descricao = models.TextField(verbose_name='Descrição',null=False)
    data_inicio = models.DateField(verbose_name='Data Inicio',null=False)
    data_fim = models.DateField(verbose_name='Data Fim',null=False)
    data_criacao = models.DateTimeField(
            default=timezone.now)

    tipoParte = models.ForeignKey(TipoParte, null=False)
    upload = models.FileField(null=True,blank=True,verbose_name='Anexo',upload_to='uploads/%Y/%m/%d/')
    boletim_interno = models.CharField(verbose_name='Boletim Interno',max_length=16,null=True,blank=True)
    data_publicacao = models.DateField(verbose_name='Data de Publicação',null=True,blank=True)
    prejuizo = models.BooleanField(verbose_name='Prejuizo a escala de serviço',default=False)
    onus = models.BooleanField(verbose_name='Com onus ao estado',default=False)
    class Meta:
        verbose_name = 'parte'
        verbose_name_plural = 'partes'
        ordering = ["author", "descricao","tipoParte"]

    def __str__(self):
        return self.descricao

    def get_absolute_url(self):
        return r('parte_new', pk=self.id)

    def queryset(self, request):
        qs = super(Parte,self).queryset(request)
        if request.author.is_superuser is False:
            return qs.filter(author=User)
        else:
            return qs

class Validacao(models.Model):
    observacao = models.TextField(null=False)
    data_autorizacao = models.DateTimeField(
            blank=True, null=True)
    parte = models.ForeignKey(Parte)
    user_validacao = models.ForeignKey('auth.User',null=True,blank=True)
    def __str__(self):
        return self.observacao

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    SOLDADO = 'Sd.'
    CABO = 'Cb.'
    SARGENTO = 'Sgt.'
    SUBTENENTE = 'SubTen.'
    TENENTE = 'Ten.'
    CAPITAO = 'Cap.'
    MAJOR = 'Maj.'
    TEN_CORONEL = 'Ten.-Cel'
    CORONEL = 'Cel.'
    HIERARQUIA = (
        (SOLDADO, 'SOLDADO'),
        (CABO, 'CABO'),
        (SARGENTO, 'SARGENTO'),
        (SUBTENENTE, 'SUBTENENTE'),
        (TENENTE, 'TENENTE'),
        (CAPITAO, 'CAPITAO'),
        (MAJOR, 'MAJOR'),
        (TEN_CORONEL, 'TEN_CORONEL'),
        (CORONEL, 'CORONEL'),
    )
    graduacao = models.CharField(max_length=32,choices=HIERARQUIA)
    nivelAutorizacao = models.ForeignKey(NivelAutorizacao)
    rg = models.CharField(max_length=9,null=False)
    setor = models.ForeignKey(Setor,blank=True,null=True)
    def __str__(self):
        return self.graduacao +" "+ self.user.first_name

class SetorParte(models.Model):
    parte = models.ForeignKey(Parte)
    setor = models.ForeignKey(Setor)
    data_enc = models.DateTimeField(null=False)
    observacao = models.TextField(null=False)