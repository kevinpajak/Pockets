from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def tempview(request, template="content/content.html"):
    cntxt, cntxt['content'] = {}, "There's nothing here for now..."
    return render(request, template, cntxt)