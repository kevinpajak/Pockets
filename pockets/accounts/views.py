from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import (login as aka_login, authenticate,
                                 logout as aka_logout, get_user_model)
from django.contrib.auth.decorators import login_required
from django.utils.http import base36_to_int
from django.contrib.auth.tokens import default_token_generator as def_token_gen

from accounts.forms import LoginForm, ProfileForm, ProfileImage
from utilities import email


User = get_user_model()


def login(request,
          just_activated=False, template="accounts/login.html"):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_user = form.save()
        aka_login(request, auth_user)
        return HttpResponseRedirect('/content/content/')
    cntxt = {'form': form, 'title': _("Login"), 'just_activated': just_activated}
    return render(request, template, cntxt)


@login_required
def logout(request):
    aka_logout(request)
    return HttpResponseRedirect('/')


def signup(request, template="accounts/signup.html"):
    form = ProfileForm(request.POST or None)
    pic = ProfileImage(request.POST, request.FILES)
    if request.method == "POST" or form.is_valid():
        new_user = form.save()
        if 'picture' in request.FILES:
            new_user.picture = request.FILES['picture']
        new_user.save()
        if not new_user.is_active:
            email.send_mail_bespoke(request, new_user, "activate")
            return HttpResponse(_("Activation email sent!"))
    cntxt = {"form": form, "pic": pic,
             "title": _("Sign Up"), "editable": False}
    return render(request, template, cntxt)


# Man...  Forget reverse!  I'll just call the friggin' view itself!

def activate_account(
        request, uidb36=None, token=None):
    id_key = base36_to_int(uidb36)
    new_user = get_object_or_404(User, id=id_key)
    if new_user is not None \
            and id_key is not None \
            and def_token_gen.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        return login(request, just_activated=True)
    else:
        return HttpResponseRedirect('/')


@login_required
def profile(
        request, template="accounts/profile.html"):
    from pockets import settings
    media_url = getattr(settings, 'MEDIA_URL', '')
    cntxt = {'img_url': media_url}
    return render(request, template, cntxt)


"""
 I'm thinking  maybe  there should be   two
 separate forms for the signup  and editing
 the profile.
"""
@login_required
def edit_profile(request, template="accounts/profile.html"):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect('/accounts/profile/')
    cntxt = {"form": form,
             "title": _("Edit Profile"), "editable": True}
    return render(request, template, cntxt)
