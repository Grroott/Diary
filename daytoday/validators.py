import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def username_validation(username):
    """
    This method validates & allows username only with Letters & Numbers.
    :param username: username from request
    :return: Raises validation error if validation fails
    """
    if not re.match(r'^[A-Za-z0-9]+$', username):
        raise ValidationError(
            _('Enter a valid username. This value may contain only letters and numbers')
        )

