from datetime import datetime
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import Account


class ChatGPTDB(models.Model):
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    user_message = models.TextField(max_length=1000, null=True, blank=True)
    ai_message = models.TextField(max_length=10000, null=True, blank=True)
    date_posted = models.DateTimeField(null=True,
        auto_now_add=True, verbose_name='date posted')

    def __str__(self):
        return f'{self.author}-{self.user_message}'


def pre_save_chatgpt_db_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        timestamp = datetime.now()
        slug_str = f'{str(instance.author.id)}-{str(timestamp)}'
        instance.slug = slugify(slug_str)

pre_save.connect(pre_save_chatgpt_db_receiver, sender=ChatGPTDB)
