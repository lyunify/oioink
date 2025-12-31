from datetime import datetime
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.utils import IntegrityError
from django.db.models import Count

from accounts.models import Account


# -------------------------------------------------------------------------------------------------
# File up load
# choices for doc location
LOCATION_CHOICES = [
    ('local', 'local'),
    ('s3', 's3'),
]

def upload_path(instance, file_name):
    file_path = f'{settings.CDN_DATA_LOCATION}/{str(instance.author.id)}/{file_name}'
    return file_path

class FileUpload(models.Model):
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    doc_location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='s3')
    doc_file = models.FileField(max_length=255, upload_to=upload_path, null=True, blank=True, unique=True)
    doc_elements = models.CharField(max_length=255, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, verbose_name='date posted')

    def __str__(self):
        return f'{self.author}'

    def save(self, *args, **kwargs):
        try:
            super(FileUpload, self).save(*args, **kwargs)
        except IntegrityError as e:
            # Handle the unique constraint violation here
            # For example, you can log the error or take appropriate action
            # You can also raise a custom exception if needed
            print(f'Error saving {self.__class__.__name__}: {e}')
        remove_duplicates()

def remove_duplicates():
    duplicates = FileUpload.objects.values('doc_file').annotate(count=Count('id')).filter(count__gt=1)
    for duplicate in duplicates:
        # Get all duplicates for the current value of 'field_to_check_for_duplicates'
        duplicate_records = FileUpload.objects.filter(doc_file=duplicate['doc_file']).order_by('-date_posted')

        # Keep the first record (most recent) and delete the rest
        first_record = True
        for record in duplicate_records:
            if first_record:
                first_record = False
            else:
                record.delete()

def pre_save_file_upload_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        timestamp = datetime.now()
        slug_str = f'{str(instance.author.id)}-{str(timestamp)}'
        instance.slug = slugify(slug_str)

pre_save.connect(pre_save_file_upload_receiver, sender=FileUpload)

# @receiver(post_delete, sender=FileUpload)
# def submission_delete(sender, instance, **kwargs):
#     instance.doc_file.delete(False)


# -------------------------------------------------------------------------------------------------
# Vector db - active and archive
class ActiveVectorDB(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    vector_db = models.CharField(max_length=30, null=True, blank=True, verbose_name='vector db')
    db_name = models.CharField(max_length=255, null=True, blank=True)
    db_elements = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.author}-{self.db_name}'


class VectorDBArchive(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    vector_db = models.CharField(max_length=30, null=True, blank=True, verbose_name='vector db')
    db_name = models.CharField(max_length=255, null=True, blank=True)
    db_elements = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')

    def __str__(self):
        return f'{self.author}-{self.db_name}'

def pre_save_vector_db_archive_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        timestamp = datetime.now()
        slug_str = f'{str(instance.author.id)}-{str(timestamp)}'
        instance.slug = slugify(slug_str)

pre_save.connect(pre_save_vector_db_archive_receiver, sender=VectorDBArchive)


# -------------------------------------------------------------------------------------------------
# LLM settings
class LLMSettings(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    llm = models.CharField(max_length=30, null=True, blank=True, verbose_name='llm')
    llm_model = models.CharField(max_length=50, null=True, blank=True, verbose_name='llm model')
    llm_api_key = models.CharField(max_length=100, null=True, blank=True, verbose_name='llm api key')
    llm_temperature = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True, verbose_name='llm temperature')
    vector_db = models.CharField(max_length=20, null=True, blank=True, verbose_name='vector db')
    vector_api_key = models.CharField(max_length=100, null=True, blank=True, verbose_name='vector api key')
    search_engine = models.CharField(max_length=20, null=True, blank=True, verbose_name='search_engine')
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')

    def __str__(self):
        return f'{self.author}-{self.vector_db}'
