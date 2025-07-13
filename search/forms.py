from django import forms

class ExcelUploadForm(forms.Form):
    fichiers = forms.FileField()
