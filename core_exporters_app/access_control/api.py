""" Set of functions to define the rules for access control across collections
"""
import logging

from core_main_app.access_control.exceptions import AccessControlError
from core_exporters_app.settings import CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT

logger = logging.getLogger(__name__)


def can_read(func, document_id, user):
    """Can user read

    Args:
        func:
        document_id:
        user:

    Returns:

    """
    if user and user.is_superuser:
        return func(document_id, user)

    if (user is None or user.is_anonymous) and not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
        raise AccessControlError("The user doesn't have enough rights.")

    if user:
        user_id = str(user.id)
    else:
        user_id = "None"

    document = func(document_id, user)
    if document.user_id == user_id:
        return document
    # user is not owner or document
    raise AccessControlError("The user doesn't have enough rights.")
