from django import forms

from .models import ChatGPTDB


class ChatGPTForm(forms.ModelForm):

    class Meta:
        model = ChatGPTDB
        fields = ['user_message', 'ai_message']
