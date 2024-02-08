from django import forms
from .models import Article, Manual


class ArticleForm(forms.ModelForm):
    manual_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Article
        fields = [
            "subject",
            "sub_text",
            "description",
            "manual_pk",  # Include this if you want to save manual_pk in your model
            "tags",
            "ordery",
            "orderx",
        ]


class ArticleDeleteForm(forms.ModelForm):
    manual_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)
    available = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Article
        fields = [
            "subject",
            "sub_text",
            "description",
            "manual_pk",  # Include this if you want to save manual_pk in your model
            "available",
        ]


class TableOfContentForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["subject", "sub_text", "ordery", "orderx"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "sub_text": forms.TextInput(attrs={"class": "form-control"}),
            "ordery": forms.NumberInput(attrs={"class": "form-control"}),
            "orderx": forms.NumberInput(attrs={"class": "form-control"}),
        }


class ManualForm(forms.ModelForm):
    class Meta:
        model = Manual
        fields = ["title", "description", "available"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
