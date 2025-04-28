from django import forms
from .models import Project, Sprint

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border rounded p-2 w-full', 'rows': 4}),
        }
    
class SprintForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Sprint
        fields = ['start_date', 'end_date'] 
