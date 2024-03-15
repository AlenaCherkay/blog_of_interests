from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, Entryform

def index(request):
  """ Домашняя страница приложения Learning log"""
  return render(request, 'learning_logs/index.html')

@login_required()
def topics(request):
  """Выводит список тем"""
  # topics = Topic.objects.order_by('date_added')
  topics = Topic.objects.filter(owner=request.user).order_by('date_added')
  context = {'topics': topics}
  return render(request,'learning_logs/topics.html', context)


@login_required()
def topic(request, topic_id):
  """Выводит одну тему и все ее записи"""
  topic = Topic.objects.get(id=topic_id)
  # Проверка того, что тема принадлежит текущему пользователю.
  if topic.owner != request.user:
    raise Http404

  # Соединение по внешнему ключю с таблицой Entry
  entries = topic.entry_set.order_by('-date_added')
  context = {'topic': topic, 'entries': entries}
  return render(request, 'learning_logs/topic.html', context)


@login_required()
def new_topic(request):
  """Определяет новую тему"""
  if request.method != 'POST':
    # Данные не отправлялись; создается пустая форма
    form =  TopicForm()
  else:
    # отправлены данные POST; обработать данные
    form = TopicForm(data=request.POST)
    if form.is_valid():
      # При первом вызове form.save() передается аргумент commit=False, потому что
      # новая тема должна быть изменена перед сохранением в базе данных
      new_topic = form.save(commit=False)
      # Атрибуту
      # owner новой темы присваивается текущий пользователь
      new_topic.owner = request.user
      new_topic.save()
      # form.save()
      return redirect('learning_logs:topics')

  # Вывести пустую или недействительную форму
  context = {'form' : form}
  return render(request, 'learning_logs/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
  """Добавляем новую запись по конкретной теме"""
  topic = Topic.objects.get(id= topic_id)
  if request.method != 'POST':
    # Данные не отправлялись; создается пустая форма
    form = Entryform()
  else:
    # отправлены данные POST; обработать данные
    form = Entryform(data=request.POST)
    if form.is_valid():
      new_entry = form.save(commit=False)
      if topic.owner != request.user:
        raise Http404
      new_entry.topic = topic
      new_entry.save()
      return redirect('learning_logs:topic', topic_id = topic_id)

  # Вывести пустую или недействительтную форму
  context = {'topic' : topic, 'form' : form}
  return render(request, 'learning_logs/new_entry.html', context)

@login_required()
def edit_entry(request, entry_id):
  """Редактирует существующую запись"""
  entry = Entry.objects.get(id=entry_id)
  # Обращение к полю topic содержащему ссылку на запист в таблице Topic
  topic = entry.topic
  if topic.owner != request.user:
    raise Http404

  if request.method != 'POST':
    # Исходный запрос, форма заполняетс яданными текущей записи
    # instance=entry  приказывает Django создать форму,
    # заранее заполненную информацией из существующего объекта записи.
    form = Entryform(instance=entry)
  else:
    # Отправка данных POST. Обработать данные
    #instance=entry и data=request.POST приказывают Django создать экземпляр формы на
    #основании информации существующего объекта записи, обновленный данными из request.POST
    form = Entryform(instance=entry, data=request.POST)
    if form.is_valid():
      form.save()
      return redirect('learning_logs:topic', topic_id=topic.id)

  context = {'entry': entry, 'topic': topic, 'form': form}
  return render(request, 'learning_logs/edit_entry.html', context)



