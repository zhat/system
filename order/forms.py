from django import forms
from .models import Advise
class AdviseForm(forms.ModelForm):
    class Meta:
        model=Advise
        fields=['summary','content']
        labels={'summary':'','content':''}