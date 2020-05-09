from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            print(key, field.label)
            if isinstance(field.widget, forms.TextInput) or \
               isinstance(field.widget, forms.Textarea) or \
               isinstance(field.widget, forms.DateInput) or \
               isinstance(field.widget, forms.DateTimeInput) or \
               isinstance(field.widget, forms.EmailInput) or\
               isinstance(field.widget, forms.TimeInput):
                if field.label == 'Username':
                    field.widget.attrs.update({'placeholder': 'Username or Email'})
                else:
                    field.widget.attrs.update({'placeholder': field.label})

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']
