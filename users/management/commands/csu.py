from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email='admin@admin.ru')
        user.set_password('admin')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()



# from django.contrib.auth import get_user_model
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         User = get_user_model()
#         if not User.objects.filter(email='admin@admin.ru').exists():
#             user = User.objects.create(
#                 email='admin@admin.ru',
#                 first_name='Admin',
#                 last_name='Admin',
#                 is_staff=True,
#                 is_superuser=True,
#                 is_active=True
#             )
#
#             user.set_password('admin')
#             user.save()
