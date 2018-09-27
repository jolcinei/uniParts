from django.contrib import admin
from .models import *

# Register your models here.

class ParteModelAdmin(admin.ModelAdmin):
    list_display = ('id','descricao','authorname','status')
    search_fields = ('descricao','tipoParte','data_criacao','author__first_name')
    list_filter = ('status','tipoParte','data_criacao','author__first_name')
    list_per_page = 10
    #actions = None
    ordering = ['author__first_name']


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('graduacao','username','setor')
    search_fields = ('nome_guerra','rg')
    actions = None
    raw_id_fields = ("user",)
    ordering = ['setor','user__first_name']
    list_filter = ('user__first_name', 'setor','graduacao')
    list_per_page = 10
    autocomplete_fields = ['user__first_name']

class TipoParteModelAdmin(admin.ModelAdmin):
    list_display = ('tpDescricao','qtd_validacoes')
    search_fields = ('tpDescricao',)
    list_per_page = 10

admin.site.register(Parte,ParteModelAdmin)
admin.site.register(TipoParte,TipoParteModelAdmin)
admin.site.register(Validacao)
admin.site.register(Alerta)
admin.site.register(NivelAutorizacao)
admin.site.register(Profile,ProfileModelAdmin)
admin.site.register(Setor)