from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.text import slugify
from django.forms import ValidationError as valderr
from django import forms


User = get_user_model()


class LoginForm(forms.ModelForm):

    err_msg = {
        'invalid': _("Invalid email and/or password!"),
        'nactive': _("Account is inactive!")
    }

    class Meta:
        model, fields = User, ('email', 'password')

    def clean(self):
        email    = self.cleaned_data['email']
        password = self.cleaned_data['password']
        self._user = authenticate(username=email, password=password)
        if self._user is None:
            raise valderr(self.err_msg['invalid'])
        elif not self._user.is_active:
            raise valderr(self.err_msg['nactive'])
        return self.cleaned_data

    def save(self):
        return getattr(self, "_user", None)


"""
 Most  of  this  form  was based on the form found
 inside  django.contrib.auth.   Figure,  the  best
 people  to emulate  would  be  the   contributors
 to Django themselves.  Of course,  I  also had to
 dig through the documentation to figure out  what
 all this clean this and clean that business is...
"""
class ProfileForm(forms.ModelForm):

    err_msg = {
        'pw_missed'  : _("Passwords don't match!")      ,
        'slugo_uname': _("User name ain't good to go!") ,
        'too_short'  : _("Password is too short!")      ,
        'em_taken'   : _("Email already registered!")   ,
        'un_taken'   : _("Username already taken!")
    }
    min_len = 4
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput)

    class Meta:
        model  = User
        fields = (
            'email'     , 'username', 'first_name',
            'last_name' , 'bio'
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        query = User.objects.filter(username__iexact=username)
        boolA, boolB = username.lower(), slugify(username).lower()
        if boolA != boolB:
            raise valderr(self.err_msg['slugo_uname'])
        if len(query) > 0:
            raise valderr(self.err_msg['un_taken'])
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise valderr(self.err_msg['pw_missed'])
        if len(password1) < self.min_len:
            raise valderr(self.err_msg['too_short'])
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        query = User.objects.filter(email__iexact=email)
        if len(query) > 0:
            raise valderr(self.err_msg['em_taken'])
        return email

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class ProfileImage(forms.ModelForm):
    # At some point, size crop features
    # should  be  added  to improve  UX
    class Meta:
        model, fields = User, ('picture',)


class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) == 0:
            raise valderr("It's blank, bub...")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) == 0:
            raise valderr("It's blank, bub...")
        return last_name

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class TermsForm(forms.Form):
    err_msg = _('You have to agree to terms!')
    tos = forms.BooleanField(
        label=_('I agree to terms.'), widget=forms.CheckboxInput,
        error_messages={'required': err_msg})


class PasswordResetForm(forms.Form):
    pass


