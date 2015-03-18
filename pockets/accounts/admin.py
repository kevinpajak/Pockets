from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms import ValidationError as valderr
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import BespokeUser


class BespokeUserCreationForm(UserCreationForm):

    class Meta:
        model = BespokeUser
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            BespokeUser._default_manager.get(username=username)
        except BespokeUser.DoesNotExist:
            return username
        raise valderr("Duplicate user!")


class BespokeUserChangeForm(UserChangeForm):

    class Meta:
        model = BespokeUser
        fields = '__all__'


class BespokeUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'bio', 'picture')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('username', 'password1', 'password2'),
        }),
    )
    add_form = BespokeUserCreationForm
    form = BespokeUserChangeForm
    ordering = ('email',)


admin.site.register(
    BespokeUser, BespokeUserAdmin
    )