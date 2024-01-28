from django import forms

from main.models import NewsLetter, Message, Client


class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ('name', 'time_mailing', 'periodicity_mailing')


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('title', 'body')


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('email', 'full_name')
