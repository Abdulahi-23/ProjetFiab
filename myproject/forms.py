# forms.py
from django import forms

class ExportForm(forms.Form):
    fichier_export = forms.FileField(label="Importer le fichier export")
