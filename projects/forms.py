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
    
class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['name','start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and start > end:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data

