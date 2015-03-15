from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import (login as aka_login, authenticate,
                                 logout as aka_logout, get_user_model)
from django.contrib.auth.decorators import login_required
from django.utils.http import base36_to_int
from django.contrib.auth.tokens import default_token_generator

from accounts.forms import LoginForm, ProfileForm, ProfileImage
from utilities import email


def login(request, template="accounts/login.html"):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_user = form.save()
        aka_login(request, auth_user)
        return HttpResponseRedirect('/content/content/')
    cntxt = {"form": form, "title": _("Log in")}
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
    cntxt = {"form": form,
             "pic": pic, "title": _("Sign up")}
    return render(request, template, cntxt)


'''
 THIS IS WHERE I'M CURRENTLY AT as of  03-13-2015!

 Ideally,   I'd   like  to  use  the  authenticate()
 method in  django.contrib.auth to   avoid importing
 the token  generator and authentication jive again,
 but I haven't been able to get it to work. Probably
 need  to make a  custom  authentication   "backend"
 function so to speak.  Anyhow, I'm having a  little
 trouble logging in, because  this  "authentication"
 doesn't seem to be good enough for the login method
 from django.contrib.auth
'''

def activate_account(request, uidb36=None, token=None):
    User = get_user_model()
    assert uidb36 is not None and token is not None
    try:
        id_key = base36_to_int(uidb36)
    except:
        raise Http404
    new_user = get_object_or_404(User, id=id_key)
    if default_token_generator.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        #user = authenticate(
        #username=new_user.username, password=new_user.password)
        #aka_login(request, user)
        return HttpResponse(_(
            "Successfully signed up"))  # Placeholder
    else:
        return HttpResponse(_(
            "Link no longer valid...")) # Placeholder


'''
 Honestly, I was a bit tired when punching this
 up.   The settings.py file should be available
 everywhere....  Maybe  I'll   try  calling  it
 straight up sometime in the near future.
'''

@login_required
def profile(
        request, template="accounts/profile.html"):
    from protoplate import settings
    media_url = getattr(settings, 'MEDIA_URL', '')
    prof_img = request.user.picture
    cntxt = {'img_url': media_url, "pic": prof_img}
    return render(
        request, template, cntxt)

