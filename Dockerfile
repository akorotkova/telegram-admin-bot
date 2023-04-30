FROM python:3.10-slim-buster

# Установка зависимостей из requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов в контейнер
COPY . /app
WORKDIR /app

# Запуск приложения
CMD python run.py
