from django.contrib import admin
from .models import *

# Register your models here.

class ParteModelAdmin(admin.ModelAdmin):
    list_display = ('descricao','author','status','data_inicio','data_fim')
    search_fields = ('descricao','tipoParte','data_criacao')
    list_filter = ('status','tipoParte','data_criacao')
  #  readonly_fields = ('status')


admin.site.register(Parte,ParteModelAdmin)
admin.site.register(TipoParte)
admin.site.register(Validacao)
admin.site.register(Alerta)
admin.site.register(NivelAutorizacao)
admin.site.register(Profile)