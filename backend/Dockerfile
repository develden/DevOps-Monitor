# Используем официальный slim-образ Python версии 3.9
FROM python:3.9-slim

# Отключаем запись .pyc и буферизацию выводов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Задаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости для работы с PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем исходный код проекта
COPY . /app/

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска приложения через gunicorn
CMD ["gunicorn", "devops_monitor.wsgi:application", "--bind", "0.0.0.0:8000"] 