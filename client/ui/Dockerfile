# Dockerfile for client project
FROM python:3.12

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Run database migrations
RUN python manage.py migrate

