

# Decided to make the homepage top most level

def index(request, template='index.html'):
    from django.shortcuts import render
    _render = render(request, template, {})
    return _render