# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port 8000 for gunicorn
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "chat_project.wsgi:application"]