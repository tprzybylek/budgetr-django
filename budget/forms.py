from django import forms
from .models import Category, Budget
from django.utils.timezone import datetime


class AddOperationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddOperationForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(label="category", queryset=Category.objects.filter(user=None) | Category.objects.filter(user=self.user), required=False)
        self.fields['budget'] = forms.ModelChoiceField(label="budget", queryset=Budget.objects.filter(user=self.user), required=False)

    datetime = forms.DateTimeField(label='Date', initial=datetime.now())
    value = forms.DecimalField(label='Value', max_digits=8, decimal_places=2)
    is_recurring = forms.BooleanField(label='is_recurring', required=False)
    is_income = forms.BooleanField(label='is_income', required=False)
    comment =  forms.CharField(widget=forms.Textarea, required=False)

class AddBudgetForm(forms.Form):
    name = forms.CharField(label='Name')
    value = forms.DecimalField(label='Start value', max_digits=8, decimal_places=2)