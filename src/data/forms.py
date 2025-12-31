from django import forms
from django.forms import ClearableFileInput

from .models import FileUpload, VectorDBArchive, ActiveVectorDB, LLMSettings


class FileUploadForm(forms.ModelForm):

    class Meta:
        model = FileUpload
        fields = ['doc_file']


class DirectoryUploadForm(forms.ModelForm):

    class Meta:
        model = FileUpload
        fields = ['doc_file']
        widgets = {
            'doc_file': ClearableFileInput(attrs={'allow_multiple_selected': True}),
        }

    def save(self, commit=True, *args, **kwargs):
        file_upload = self.instance
        file_upload.doc_file = self.cleaned_data['doc_file']
        file_upload = super().save(commit=False, *args, **kwargs)
        if commit:
            file_upload.save()
        return file_upload


class CSVUploadForm(forms.ModelForm):

    class Meta:
        model = FileUpload
        fields = ['doc_file', 'doc_elements']


class WebBaseUploadForm(forms.ModelForm):

    class Meta:
        model = FileUpload
        fields = ['doc_file']


class OnlinePDFUploadForm(forms.ModelForm):

    class Meta:
        model = FileUpload
        fields = ['doc_file']


class VectorDBForm(forms.ModelForm):

    class Meta:
        model = LLMSettings
        fields = ['llm', 'llm_model', 'vector_db']


class VectorDBUpdateForm(forms.ModelForm):

    class Meta:
        model = LLMSettings
        fields = ['llm', 'llm_model', 'vector_db']

    def save(self, commit=True, *args, **kwargs):
        llm_settings = self.instance
        llm_settings.llm = self.cleaned_data['llm']
        llm_settings.vector_db = self.cleaned_data['vector_db']
        llm_settings = super().save(commit=False, *args, **kwargs)
        if commit:
            llm_settings.save()
        return llm_settings


class ActiveVectorDBForm(forms.ModelForm):

    class Meta:
        model = ActiveVectorDB
        fields = ['vector_db', 'db_name', 'db_elements']


class VectorDBArchiveForm(forms.ModelForm):

    class Meta:
        model = VectorDBArchive
        fields = ['vector_db', 'db_name', 'db_elements']


class LLMSettingsForm(forms.ModelForm):

    class Meta:
        model = LLMSettings
        fields = ['llm', 'llm_model', 'llm_api_key', 'llm_temperature', 
                  'vector_db', 'vector_api_key', 'search_engine']

    def save(self, commit=True, *args, **kwargs):
        llm_settings = self.instance
        input_string = self.cleaned_data['llm_model']
        string_list = input_string.split(' ')
        llm_settings.llm = string_list[0]
        llm_settings.llm_model = string_list[1]
        llm_settings.llm_api_key = self.cleaned_data['llm_api_key']
        llm_settings.vector_db = self.cleaned_data['vector_db']
        llm_settings.vector_api_key = self.cleaned_data['vector_api_key']
        llm_settings.search_engine = self.cleaned_data['search_engine']
        llm_settings = super().save(commit=False, *args, **kwargs)
        if commit:
            llm_settings.save()
        return llm_settings


class LLMSettingsUpdateForm(forms.ModelForm):

    class Meta:
        model = LLMSettings
        fields = ['llm', 'llm_model', 'llm_api_key', 'llm_temperature', 
                  'vector_db', 'vector_api_key', 'search_engine']

    def save(self, commit=True, *args, **kwargs):
        llm_settings = self.instance
        input_string = self.cleaned_data['llm_model']
        string_list = input_string.split(' ')
        llm_settings.llm = string_list[0]
        llm_settings.llm_model = string_list[1]
        llm_settings.llm_api_key = self.cleaned_data['llm_api_key']
        llm_settings.vector_db = self.cleaned_data['vector_db']
        llm_settings.vector_api_key = self.cleaned_data['vector_api_key']
        llm_settings.search_engine = self.cleaned_data['search_engine']
        llm_settings = super().save(commit=False, *args, **kwargs)
        if commit:
            llm_settings.save()
        return llm_settings
