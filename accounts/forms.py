from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from .models import User, Profile
from django.db import transaction

GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]


class UserCreationForm(SignupForm):
    is_consumer = forms.BooleanField(label="Patient?", initial=True, required=False)
    whichapp = forms.BooleanField(label="CBCT", initial=True, required=False)
    is_terms = forms.BooleanField(
        label="I agree to the terms and conditions", initial=True, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password"}
        )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "is_consumer",
            "whichapp",
            "is_terms",
        )

    def save(self, request):
        user = super(UserCreationForm, self).save(request)
        user.is_consumer = self.cleaned_data.get("is_consumer")
        user.whichapp = self.cleaned_data.get("whichapp")
        user.is_terms = self.cleaned_data.get("is_terms")
        user.save()
        return user


class UserChangeForm(UserChangeForm):
    password = None
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)

    class Meta:
        model = Profile
        fields = (
            "bio",
            "cellphone",
            "birth_date",
            "gender",
            "address",
            "suite",
            "city",
            "state",
            "zipcode",
            "country",
        )
