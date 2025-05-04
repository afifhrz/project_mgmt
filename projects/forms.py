from django import forms
from .models import Project, Sprint
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Button

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
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field("name", css_class="mb-4"),
            Field("start_date", css_class="mb-4"),
            Field("end_date", css_class="mb-4"),
            Div(Layout(
                Submit("submit", "Save", css_class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"),
                Button("name", css_class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700", value="Cancel", onclick="document.getElementById('modal').style.display='none'"),
            ), css_class="flex justify-end gap-2 mt-4"),
        )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and start > end:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data

