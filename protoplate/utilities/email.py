from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import loader, Context


'''
 Okay...  The realization there's some hard-coding
 is not lost upon me here. If this ever goes live;
 be rest  assured user,  the  hard-coding  will be
 removed.
'''

def send_mail_bespoke(request, user, view_to_a_kill):
    actvte_url = reverse(view_to_a_kill, kwargs={
        "uidb36": int_to_base36(user.id),
        "token": default_token_generator.make_token(user),
        }) + "?next=ACCOUNT_WILLBE_ACTIVATED!"
    subj, frome, toe = 'Hello Christopher...', 'from@example.com', 'to@example.com'
    content = lambda toh: loader \
        .get_template("%s.%s" % ('email/activation', toh)) \
        .render(Context({'host': request.get_host, 'actv_url': actvte_url}))
    msg = EmailMultiAlternatives(subj, content("txt"), frome, [toe])
    msg.attach_alternative(content("html"), "text/html")
    msg.send()


# It helps me sometimes to  code it out in
# a dumb manner...  That  way I understand
# what the heck I'm doing with that lambda
# and/or anonymous function I use here.

'''
def send_mail_bespoke(request):
    subj, frome, toe = 'Hello Christopher...', 'from@example.com', 'to@example.com'
    content = lambda toh: loader\
        .get_template("%s.%s" % ('email/activation', toh))\
        .render(Context({'host': request.get_host, 'some_url': 'something.com'}))
    msg = EmailMultiAlternatives(subj, content("txt"), frome, [toe])
    msg.attach_alternative(content("html"), "text/html")
    msg.send()


def send_mail_bespoke(request):
    subject, from_email, to = 'Hello Christopher!', 'from@example.com', 'to@example.com'

    txt_temp = loader.get_template('email/activation.txt')
    txt_cntxt = Context({'host': request.get_host, 'some_url': 'something.com'})
    txt_content = txt_temp.render(txt_cntxt)

    html_temp = loader.get_template('email/activation.html')
    html_cntxt = Context({'host': request.get_host, 'some_url': 'something.com'})
    html_content = html_temp.render(html_cntxt)

    msg = EmailMultiAlternatives(subject, txt_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
'''


