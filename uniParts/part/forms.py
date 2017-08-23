from django import forms

from .models import *

class ParteForm(forms.ModelForm):
    class Meta:
        model = Parte
        fields = ('tipoParte','upload','descricao','data_inicio','data_fim',)

class ValidacaoForm(forms.ModelForm):
    class Meta:
        model = Validacao
        fields = ('observacao','nivelAutorizacao',)
