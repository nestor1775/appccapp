from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress
from allauth.account.forms import ResetPasswordForm
from django.contrib.sites.shortcuts import get_current_site


def send_confirmation_email(request, user):
    """
    Envía un email de confirmación al usuario.
    """
    send_email_confirmation(request, user)

def resend_confirmation_email(request, email):
    """
    Reenvía email de confirmación si no ha verificado aún.
    """
    try:
        email_obj = EmailAddress.objects.get(email=email)
        if not email_obj.verified:
            send_email_confirmation(request, email_obj.user)
            return True
        return False
    except EmailAddress.DoesNotExist:
        return False

def send_password_reset_email(request, email):
    """
    Envía un email de reseteo de contraseña al usuario.
    Devuelve True si se envió, False si el email no existe.
    """
    form = ResetPasswordForm(data={"email": email})
    if form.is_valid():
        form.save(
            request=request,
            use_https=request.is_secure(),
            from_email=None,  # usa el DEFAULT_FROM_EMAIL
            email_template_name='account/password_reset_email.html',
            extra_email_context=None,
        )
        return True
    return False


