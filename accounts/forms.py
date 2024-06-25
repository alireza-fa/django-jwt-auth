from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('password'), widget=forms.PasswordInput())
    password2 = forms.CharField(
        label=_('confirm password'), widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('fullname', 'national_code', 'phone_number', 'email', 'avatar_image')

    def clean_password2(self):
        password1, password2 = self.cleaned_data.get(
            'password1'), self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('passwords don\t match'))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text=_(
            'you can change password using <a href="../password/">this link</a>')
    )

    class Meta:
        model = get_user_model()
        fields = (
            'fullname', 'national_code', 'phone_number', 'email', 'is_active', 'is_admin', 'is_superuser', 'last_login'
        )
