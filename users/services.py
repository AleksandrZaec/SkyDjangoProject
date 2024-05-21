import random
from django.core.mail import send_mail
from django.conf import settings

class UserService:
    @staticmethod
    def generate_verification_code(length=9):
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    @staticmethod
    def send_verification_email(user):
        send_mail(
            subject='Подтверждение почты',
            message=f'Код {user.ver_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )