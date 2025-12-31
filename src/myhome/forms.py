from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=60, required=True)
    name = forms.CharField(max_length=30, required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            return email

    def clean_name(self):
        if self.is_valid():
            name = self.cleaned_data['name']
            return name

    def clean_subject(self):
        if self.is_valid():
            subject = self.cleaned_data['subject']
            return subject

    def clean_message(self):
        if self.is_valid():
            message = self.cleaned_data['message']
            return message
