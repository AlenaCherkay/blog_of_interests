from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
  class Meta:
    # На какой модели базируется форма
    model = Topic
    # Поля
    fields = ['text']
    # Подписи для текстового поля
    labels = {'text' : ''}


class Entryform(forms.ModelForm):
  class Meta:
    model = Entry
    fields = ['text']
    labels = {'text': 'Entry:'}
    widgets = {'text': forms.Textarea(attrs={'cols': 80})}