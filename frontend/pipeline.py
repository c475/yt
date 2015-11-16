from django.http import HttpResponseRedirect
from social.exceptions import AuthException

from credentials import ALLOWED_DOMAINS
from backend.models import User


def create_if_nonexistent(details, *args, **kwargs):
    email = details.get("email")

    if email is not None:
        name, domain = email.split("@")
        if domain in ALLOWED_DOMAINS:
            if not User.objects.filter(email=email).exists():
                User.objects.create(
                    email=email,
                    username=name
                )


def associate_by_email(backend, details, user=None, *args, **kwargs):
    if user:
        return None

    users = User.objects.filter(email=details.get('email', '').lower()).all()

    if len(users) == 0:
        return None

    elif len(users) > 1:
        raise AuthException(
            backend,
            'The given email address is associated with another account'
        )

    else:
        return {'user': users[0]}


def login_check(details, *args, **kwargs):
    if not User.objects.filter(email=details['email'].lower()).exists():
        return HttpResponseRedirect('/login/')
