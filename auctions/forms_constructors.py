from django import forms
from . import models

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=255, required=True)
    starting_bid = forms.FloatField(required=True, min_value=1)
    image_url = forms.CharField(max_length=255, required=False)
    category = forms.ModelChoiceField(
        queryset=models.Category.objects.all(),
        empty_label="Select a Category"
    )
