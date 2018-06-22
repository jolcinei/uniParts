from django.contrib import admin
from .models import *

# Register your models here.

class ParteModelAdmin(admin.ModelAdmin):
    list_display = ('descricao','authorname','status')
    search_fields = ('descricao','tipoParte','data_criacao','author__first_name')
    list_filter = ('status','tipoParte','data_criacao','author__first_name')
    actions = None
    ordering = ['author__first_name']


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('graduacao','username','setor')
#    search_fields = ('graduacao','user__first_name','setor')
    actions = None
    raw_id_fields = ("user",)
    ordering = ['setor','user__first_name']
    list_filter = ('user__first_name', 'setor')
    list_per_page = 10
    autocomplete_fields = ['user__first_name']


admin.site.register(Parte,ParteModelAdmin)
admin.site.register(TipoParte)
admin.site.register(Validacao)
admin.site.register(Alerta)
admin.site.register(NivelAutorizacao)
admin.site.register(Profile,ProfileModelAdmin)
admin.site.register(Setor)