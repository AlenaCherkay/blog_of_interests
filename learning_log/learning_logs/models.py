from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
  """Модель описывает таблицу хранящую : темы которые изучает пользлватель"""
  text = models.CharField(max_length=200)
  date_added = models.DateField(auto_now_add=True)
  # бавляется поле owner, используемое в отношении внешнего ключа к модели User
  owner = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    """Возвращает строковое представление модели"""
    return self.text


class Entry(models.Model):
  """Модель описывает таблицу хранящую :информацию изученную пользователем по теме"""
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
  text = models.TextField()
  date_added = models.DateField(auto_now_add=True)

  class Meta:
    # Класс хранит дополнительную информацию по управлению моделью
    # Позволяет задать форму множественного числа
    verbose_name_plural = 'entries'

  def __str__(self):
    """Возвращает строовое представление модели"""
    if len(self.text) >= 50:
      return f"{self.text[:50]}..."
    else:
      return f"{self.text}"
