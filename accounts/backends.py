# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        if username_or_email is None or password is None:
            return None

        try:
            # Try to fetch the user by email or username
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user

        return None
