from django import forms
from .models import Senha
from datetime import timedelta

class SenhaForm(forms.ModelForm):
    numero_dias = forms.IntegerField(required=False, min_value=1, label="Ou número de dias")

    class Meta:
        model = Senha
        fields = ['equipamento', 'tipo', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        numero_dias = cleaned_data.get('numero_dias')

        if tipo == 'temporaria':
            if numero_dias and data_inicio:
                cleaned_data['data_fim'] = data_inicio + timedelta(days=numero_dias)
            elif not data_fim:
                raise forms.ValidationError('Informe data fim ou número de dias')

        if tipo == 'definitiva':
            cleaned_data['data_fim'] = None

        return cleaned_data
