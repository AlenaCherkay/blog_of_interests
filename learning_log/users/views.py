from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
  """Регистрация нового пользователя"""
  if request.method != 'POST':
    # Выврдит пустую форму регистрации.
    form = UserCreationForm()
  else:
    # Обработка заполненной формы
    form = UserCreationForm(data=request.POST)

    if form.is_valid():
      new_user = form.save()
      # Выполнение выхода и прернапрвление на домашнюю страницу
      login(request, new_user)
      return redirect('learning_logs:index')

  # Вывести пустую или недействительную форму
  context = {'form': form}
  return render(request, 'users/register.html', context)


def register2(request):
  """ Домашняя страница приложения Learning log"""
  return render(request, 'users/register2.html')