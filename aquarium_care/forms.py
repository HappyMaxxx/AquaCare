from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from  django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django import forms

class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        error_messages = {
            'username': {
                'unique': 'Користувач з таким ім\'ям вже існує'
            },
        }
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Паролі не співпадають", code='password_mismatch')
        return password2
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        
class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

        self.error_messages['invalid_login'] = "Введено неправильне ім'я користувача або пароль. Зверніть увагу, що обидва поля чутливі до регістру."

class PincodeForm(forms.Form):
    pincode = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={'class': 'form-control'}))