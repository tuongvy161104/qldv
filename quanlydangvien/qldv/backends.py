from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    """Custom authentication backend để đăng nhập bằng email thay vì username"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Xác thực người dùng bằng email hoặc username và mật khẩu"""
        identifier = username or kwargs.get("email") or kwargs.get("username")
        if not identifier or password is None:
            return None

        user = None
        if "@" in identifier:
            user = User.objects.filter(email__iexact=identifier).order_by("pk").first()
        else:
            user = User.objects.filter(username__iexact=identifier).order_by("pk").first()
            if user is None:
                user = User.objects.filter(email__iexact=identifier).order_by("pk").first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        """Lấy người dùng bằng user_id"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
