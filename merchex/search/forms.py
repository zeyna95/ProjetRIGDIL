from re import search
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", 'first_name', 'last_name', "password1",
                  "password2", "pays", "sexe", "matrimoniale", "profession")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.pays = self.cleaned_data['pays']
        user.sexe = self.cleaned_data['sexe']
        user.matrimoniale = self.cleaned_data['matrimoniale']
        user.profession = self.cleaned_data['profession']

        if commit:
            user.save()
        return user


class SearchForm(forms.Form):

    search = forms.CharField(label='Search', max_length=1000)
    profil = forms.CharField(label='profil', max_length=10)
