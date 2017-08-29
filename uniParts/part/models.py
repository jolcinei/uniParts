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

class NivelAutorizacao(models.Model):
    SUP='superior'
    SUB='subcomando'
    COM='comando'
    NIVEL = (
        (SUP, 'SUPERIOR'),
        (SUB, 'SUBCOMANDO'),
        (COM, 'COMANDO'),
    )
    nivel = models.CharField(max_length=20,choices=NIVEL)
    def __str__(self):
        return str(self.nivel)

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

    tipoParte = models.ForeignKey(TipoParte)
    upload = models.FileField(null=True,blank=True,verbose_name='Anexo',upload_to='uploads/%Y/%m/%d/')
    boletim_interno = models.CharField(verbose_name='Boletim Interno',max_length=16,null=True,blank=True)
    data_publicacao = models.DateTimeField(verbose_name='Data de Publicação',null=True,blank=True)

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
    nivelAutorizacao = models.ForeignKey(NivelAutorizacao)
    parte = models.ForeignKey(Parte)

    def __str__(self):
        return self.observacao

