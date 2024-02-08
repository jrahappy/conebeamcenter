from django import forms
from .models import ICase, ICaseDetail, ICaseImage, TPlan, TPlanDetail


class ICaseForm(forms.ModelForm):
    name = forms.CharField(
        label="Case title",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "style": "margin-bottom:10px"}
        ),
    )
    bodypart = forms.CharField(
        label="Body part",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "style": "margin-bottom:10px"}
        ),
        required=False,
    )
    description = forms.CharField(
        label="Case description",
        widget=forms.Textarea(
            attrs={"class": "form-control", "style": "margin-bottom:10px", "rows": 3}
        ),
    )
    status = forms.ChoiceField(
        choices=ICase.STATUS_CHOICES,
        label="Case status",
        initial="Draft",
        widget=forms.Select(
            attrs={"class": "form-control", "style": "width:200px;margin-bottom:10px"}
        ),
    )
    report = forms.FileField(
        label="File Upload",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "style": "margin-bottom:10px",
                "multiple": False,
            }
        ),
        required=False,
    )
    tags = forms.CharField(
        label="Tags",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "style": "margin-bottom:10px"}
        ),
        required=False,
    )

    class Meta:
        model = ICase
        fields = ["name", "bodypart", "description", "status", "report", "tags"]


class TPlanForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    cost = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.00)
    terms = forms.IntegerField()
    visits = forms.IntegerField()

    class Meta:
        model = TPlan
        fields = ["name", "description", "cost", "terms", "visits"]
