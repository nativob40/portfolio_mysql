from django import forms


class Formulario_traduccion_ingles(forms.Form):
    verbo = forms.CharField(max_length=40)
    verbo_traducido = forms.CharField(max_length=40)


class Formulario_conjugacion_ingles(forms.Form):
    verbo = forms.CharField(max_length=40)
