from django.contrib.auth.backends import BaseBackend

from .models import User


class UserBackend(BaseBackend):
    def authenticate(self, request, email, password):
        qs = User.objects.prefetch_related('organisations')
        try:
            user = qs.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user

        return None

    def get_user(self, user_id):
        qs = User.objects.prefetch_related('organisations')
        try:
            return qs.get(pk=user_id)
        except User.DoesNotExist:
            return None
