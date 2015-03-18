from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils import timezone


"""
I've inherited from  the  auth UserManager and
have only overridden one  method in the class.
It's probably a bit dangerous to override like
this too frequently, but here...  I think I'll
take the chance  for the sake of  having  less
lines of code.
"""
class BespokeUserManager(UserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Given email gotta be set!')
        if not username:
            raise ValueError('Given username gotta be set!')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                           date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


"""
Just for the moment. Probably will change
the fields in the future.  I  think a bio
isn't terribly required.
"""
class BespokeUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=32, unique=True,
                                help_text=_('Required. 32 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                                              _('Enter a valid username. '
                                                                'This value may contain only letters, numbers '
                                                                'and @/./+/-/_ characters.'), 'invalid'),
                                    ],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                    }
                                )
    first_name = models.CharField(_('first name'), max_length=32, blank=True)
    last_name = models.CharField(_('last name'), max_length=32, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                help_text=_('Designates whether the user can log into this admin '
                                           'site.'))
    is_active = models.BooleanField(_('active'), default=False,
                                help_text=_('Designates whether this user should be treated as '
                                            'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    bio = models.CharField(max_length=1000, blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    objects = BespokeUserManager()
    USERNAME_FIELD, REQUIRED_FIELDS = 'email' ,['username']

    def get_short_name(self):
        # Do I even want to bother with this?
        return self.first_name

    def __str__(self):
        return self.email