# DevOps Monitor

## Описание проекта
DevOps Monitor — это комплексное решение для мониторинга процессов CI/CD, управления сборками и интеграции с внешними системами. Проект объединяет мощный Backend, разработанный на Django и Django REST Framework, с современным Frontend, реализованным на React, а также включает в себя интеграционные сервисы, уведомления и аналитику.

## Основные возможности
- **API для управления сборками**: создание, отслеживание и логирование сборок.
- **Уведомления**: отправка уведомлений через Email, Slack и Telegram.
- **Аналитика**: анализ времени сборок, выявление трендов и аномалий.
- **Контейнеризация**: поддержка Docker, docker-compose для локальной разработки и Kubernetes для продакшена.
- **CI/CD**: автоматизированный пайплайн на GitHub Actions для сборки, тестирования и деплоя.
- **Документация API**: Swagger (drf-yasg) для подробного описания эндпоинтов.

## Структура проекта
- **backend/**  
  Содержит исходный код приложения на Django, API, модели, интеграционные методы и тесты.
- **frontend/**  
  Реализован на React. Включает пользовательский интерфейс с дашбордом, инструментами управления сборками и визуализацией аналитики.
- **docs/**  
  Техническая документация для разработчиков, описание архитектуры и интеграционных процессов.
- **docker-compose.yml**  
  Конфигурация для локальной разработки с использованием Docker.
- **.github/workflows/**  
  Пайплайн CI/CD для автоматизации сборки, тестирования и деплоя.
- **k8s/**  
  Манифесты для деплоя в Kubernetes (Deployment, Service, Ingress).

## Установка и запуск

### Локальное окружение
1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/yourusername/devops-monitor.git
   cd devops-monitor
   ```

2. **Настройка переменных окружения**  
   Создайте файл `.env` в корневой директории и задайте следующие переменные:
   ```bash
   DEBUG=1
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgres://postgres:postgres@db:5432/devops_monitor
   REDIS_URL=redis://redis:6379/0
   SMTP_HOST=smtp.yourhost.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@example.com
   SMTP_PASSWORD=your_password
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

3. **Запуск docker-compose**  
   Для сборки и запуска всех сервисов выполните:
   ```bash
   docker-compose up --build
   ```
   - **Backend** запустится на [http://localhost:8000](http://localhost:8000)
   - **Frontend** доступен по [http://localhost:3000](http://localhost:3000)
   - **Swagger документация API**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

### Локальное тестирование
- **Тестирование Backend**  
  В каталоге `backend` выполните:
  ```bash
  python manage.py test
  ```

- **Тестирование Frontend**  
  Для запуска UI тестов через Cypress:
  ```bash
  cd frontend
  npx cypress open
  ```

- **Нагрузочное тестирование**  
  Используйте Locust:
  ```bash
  locust --host=http://localhost:8000
  ```
  Перейдите на [http://localhost:8089](http://localhost:8089) для запуска тестовой сессии.

## Руководство для пользователей и администраторов

### Для пользователей
- **Авторизация**: Вход в систему осуществляется с использованием зарегистрированных учетных записей.
- **Работа с дашбордом**: Просмотр состояния сборок, фильтрация по критериям.
- **Управление сборками**: Запуск новых сборок и просмотр логов текущих.

### Для администраторов
- **Управление пользователями**: Настройка прав доступа и контроль учетных записей.
- **Интеграция с CI/CD системами**: Конфигурация Jenkins, GitHub Actions, GitLab CI для автоматизации сборок.
- **Мониторинг уведомлений**: Анализ и настройка уведомлений через Email, Slack, Telegram.
- **Аудит и безопасность**: Проведение аудита, настройка статического анализа кода и инструментов мониторинга.

## Деплой и финальное тестирование
1. **Тестовое окружение**  
   Разверните тестовую копию проекта с использованием Docker или Kubernetes.

2. **Финальные проверки**  
   - Проведите интеграционные и нагрузочные тестирования.
   - Выполните аудит безопасности (проверьте защиту от SQL-инъекций, XSS, CSRF).

3. **Сборка и релиз**  
   Создайте окончательные Docker-образы и задеплойте их в продакшн среду (например, через Kubernetes). Окончательный релиз производится после прохождения всех тестов и проверки соответствия требованиям.

## Документация API
- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Redoc UI**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Советы по развитию и поддержке
- **CI/CD интеграция**: Используйте автоматизированный пайплайн на GitHub Actions для проверки кода, запуска тестов и сборки.
- **Мониторинг и логирование**: Настройте интеграцию с системами мониторинга (Sentry, Prometheus) для оперативного обнаружения и устранения ошибок.
- **Обновления безопасности**: Регулярно проводите аудит кода с использованием Bandit, ESLint и аналогичных инструментов.
