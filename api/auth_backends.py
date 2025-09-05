from django.contrib.auth.backends import ModelBackend
from api.models.user import User 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError




class EmailBackend(ModelBackend):
    """
    Autentica solo usando email y contraseña, incluso si is_active=False.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None

        # Validar que sea un email
        try:
            validate_email(email)
        except ValidationError:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user  # aunque is_active=False
        return None




