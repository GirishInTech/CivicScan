from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Full Name', max_length=100)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']

        if commit:
            user.save()
            # Save phone number to UserProfile
            phone = self.cleaned_data['phone_number']
            UserProfile.objects.create(user=user, phone_number=phone)

        return user
