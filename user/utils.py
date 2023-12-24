from rest_framework.exceptions import ValidationError

SIGN = "!@#$%^&*()_-+=<>?/[]{}|"
LOWERCASE = "abcdefghijklmnopqrstuvwxyz"


def equal_username_view(username, new_password):
    uppercase_count = sum(1 for char in new_password if char.isupper())

    if username.upper() == new_password.upper():
        raise ValidationError({'success': False, 'message': "Username va parol bir xil bo'lmasligi kerak"})
    elif not any(char in SIGN for char in new_password):
        raise ValidationError({'success': False, 'message': "Belgi iborat bo'lishi kerak"})
    elif not any(char in LOWERCASE for char in new_password):
        raise ValidationError({'success': False, 'message': "Kichik harfdan iborat bo'lishi kerak"})
    elif uppercase_count < 2:
        raise ValidationError({"success": False, "message": "Parol kamida 2 ta katta harf bo'lishi kerak"})
    elif not username:
        raise ValidationError({'success': False, 'message': "Username kiritmadingiz"})
    else:
        return True
