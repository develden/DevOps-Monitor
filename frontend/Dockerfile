# Используем официальный образ Node.js LTS
FROM node:14

# Задаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json для установки зависимостей
COPY package.json package-lock.json ./
RUN npm install

# Копируем исходный код проекта
COPY . /app/

# Сбор статики (если требуется)
RUN python manage.py collectstatic --noinput

# Собираем проект
RUN npm run build

# Открываем порт 8000
EXPOSE 8000

# Добавляем HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8000/ || exit 1

# Команда для запуска приложения через gunicorn
CMD ["gunicorn", "devops_monitor.wsgi:application", "--bind", "0.0.0.0:8000"] 