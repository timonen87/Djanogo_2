from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta

from django.core.mail import send_mail
from django.conf import settings
from authapp.models import ShopUser



class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)

    age = models.PositiveIntegerField(verbose_name = 'возраст', default = '18')

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))


    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    def send_verify_mail(user):
        verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
        
        title = f'Подтверждение учетной записи {user.username}'

        message = f'Для подтверждения учетной записи {user.username} на портале \
        {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
        
        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

