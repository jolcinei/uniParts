from django import forms
from .models import *

class ParteForm(forms.ModelForm):
    class Meta:
        model = Parte
        fields = ('tipoParte','upload','descricao','data_inicio','data_fim',)
        widgets = {
            #'tipoParte' : forms.ModelChoiceField(queryset=TipoParte.objects.all()),
            'data_inicio': forms.DateInput(attrs={'class':'datepicker'}),
            'data_fim': forms.DateInput(attrs={'class':'datepicker'}),
        }

class ValidacaoForm(forms.ModelForm):
    class Meta:
        model = Validacao
        fields = ('observacao',)

class ParteValidacaoForm(forms.ModelForm):
    class Meta:
        model = Parte
        fields = ('boletim_interno','data_publicacao',)
        widgets = {
            'data_publicacao' : forms.DateInput(attrs={'class':'datepicker'},),
        }



