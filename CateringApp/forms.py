from django import forms
from .models import *

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'