from django import forms
from .models import OrderCrawl
class OrderCrawlForm(forms.ModelForm):
    class Meta:
        model=OrderCrawl
        fields=['asin','name','profile','zone','days']
        labels={'asin':'','name':'','profile':'','zone':'','days':''}