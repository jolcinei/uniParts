from django import forms
from .models import *


class ParteForm(forms.ModelForm):
    class Meta:
        model = Parte
        fields = ('tipoParte','upload','descricao',)
#        widgets = {
#            'data_inicio': forms.DateInput(attrs={'class':'datepicker'}),
#            'data_fim': forms.DateInput(attrs={'class':'datepicker'}),
#        }

class ValidacaoForm(forms.ModelForm):
    class Meta:
        model = Validacao
        fields = ('observacao',)

class SetorParteForm(forms.ModelForm):
    class Meta:
        model = SetorParte
        fields = ('setor',)

class ParteValidacaoForm(forms.ModelForm):
    class Meta:
        model = Parte
        fields = ('boletim_interno','data_publicacao',)
        widgets = {
            'data_publicacao' : forms.DateInput(attrs={'class':'datepicker'},),
        }
