from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_email_unique(value):
    exists = User.objects.filter(username=value)
    if exists:
        raise ValidationError("Email address %s already exits, must be unique" % value)
        print("ERROR DE EMAIL")
