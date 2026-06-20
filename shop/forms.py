from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, Review


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "phone",
            "street",
            "postal_code",
            "city",
        ]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "rating",
            "comment",
        ]

        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }

