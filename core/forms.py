from django import forms
from pyairtable.formulas import match

from core.services import decrypt
from django_aiogram_airtable.settings import table


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.widgets.PasswordInput())

    def clean(self):
        formula = match(
            {
                "username": self.cleaned_data['username'],
            }
        )
        user = table.first(formula=formula)

        if not user:
            raise forms.ValidationError('Incorrect username')
        if decrypt(user.get("fields").get("password")) != self.cleaned_data["password"]:
            raise forms.ValidationError('Incorrect password')

