from django import forms
from .models import *

class ParteForm(forms.ModelForm):
    class Meta:
        model = Parte
        fields = ('tipoParte','upload','descricao','data_inicio','data_fim',)
        widgets = {
            #'tipoParte' : forms.ModelChoiceField(queryset=TipoParte.objects.all()),
            'data_inicio': forms.DateInput(attrs={'type' : 'date'}),
            'data_fim': forms.DateInput(attrs={'class':'datepicker'}),
        }

class ValidacaoForm(forms.ModelForm):
    #nivelAutorizacao = forms.ModelChoiceField(queryset=NivelAutorizacao.objects.all())
    class Meta:
        model = Validacao
        fields = ('observacao','nivelAutorizacao',)

class ParteValidacaoForm(forms.ModelForm):
    class Meta:
        model = Parte
        fields = ('boletim_interno','data_publicacao',)
        widgets = {
            'data_publicacao' : forms.DateInput(attrs={'type': 'date'},),
        }



