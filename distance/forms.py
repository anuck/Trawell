from django import forms
from .models import Distance

class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model= Distance
        fields = ('destination',)
