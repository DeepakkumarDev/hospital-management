from django.core.exceptions import ValidationError

def validate_age(age):
    if age<=0:
        raise ValidationError(f"age can not be less then equal to {0}")