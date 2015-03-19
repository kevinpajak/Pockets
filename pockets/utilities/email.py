from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import loader, Context


"""
 Okay...  The realization there's some hard-coding
 is not lost upon me here. If this ever goes live;
 be rest  assured user,  the  hard-coding  will be
 removed.
"""
def send_mail_bespoke(request, user, view_to_a_kill):
    actvte_url = reverse(view_to_a_kill, kwargs={
        "uidb36": int_to_base36(user.id),
        "token": default_token_generator.make_token(user),
        }) + "?next=ACTIVATION!"
    subj, frome, toe = 'Hello Christopher...', 'from@example.com', 'to@example.com'
    content = lambda toh: loader \
        .get_template("%s.%s" % ('email/activation', toh)) \
        .render(Context({'host': request.get_host, 'actv_url': actvte_url}))
    msg = EmailMultiAlternatives(subj, content("txt"), frome, [toe])
    msg.attach_alternative(content("html"), "text/html")
    msg.send()
