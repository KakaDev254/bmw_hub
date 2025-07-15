from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


def send_verification_email(request, user):
    """
    Sends an account activation email with a verification link.
    """
    current_site = get_current_site(request)
    mail_subject = 'Activate your BMWPartsHub account'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://{current_site.domain}/accounts/activate/{uid}/{token}/"

    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'activation_link': activation_link,
    })

    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
