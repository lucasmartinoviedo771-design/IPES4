# academia_core/forms_espacios.py
from django import forms

from .models import EspacioCurricular


class EspacioForm(forms.ModelForm):
    class Meta:
        model = EspacioCurricular
        fields = [
            "plan",
            "anio",
            "cuatrimestre",
            "formato",
            "materia",
            "horas",
        ]
        widgets = {
            "anio": forms.TextInput(attrs={"placeholder": "1° / 2° / 3° / 4°"}),
        }
