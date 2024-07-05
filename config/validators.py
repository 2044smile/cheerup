from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re
 
 
class CustomPasswordValidator:
    def __call__(self, value): # 1)
        try:
            validate_password(value)
        except ValidationError as e:
            raise ValidationError(str(e))
 
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("비밀번호는 8자리 이상이어야 합니다.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("비밀번호는 소문자를 포함해야 합니다.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("비밀번호는 대문자를 포함해야 합니다.")
        if not re.search(r"[!@#$%^&*()]", password):
            raise ValidationError("비밀번호는 특수문자를 포함해야 합니다.")
 
    def get_help_text(self): # 2)
        return "비밀번호는 8자리 이상이며 영문, 숫자, 특수문자((!@#$%^&*()))를 포함해야 합니다"
    