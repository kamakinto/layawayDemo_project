from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class LoginForm(forms.Form):
        username = forms.CharField(
                widget=forms.TextInput(
                        attrs={
                                "class": "form-control",
                                "placeholder":"Your Username",
                                "id":"form_username"
                        }
                )
        )
        password = forms.CharField(
                widget=forms.PasswordInput(
                        attrs={
                                "class":"form-control",
                        }
                )

                )