from django import forms
from django.contrib.auth.models import User
from .models import Users


class UserForm(forms.ModelForm):
    username = forms.CharField(label='User Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        data = self.cleaned_data['email']
        duplicate_users = User.objects.filter(email=data)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_users = duplicate_users.exclude(pk=self.instance.pk)
        if duplicate_users.exists():
            raise forms.ValidationError("Email has already registered")
        return data

class UserRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(label='Full Name:', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta():
        model = Users
        fields = ('full_name',)