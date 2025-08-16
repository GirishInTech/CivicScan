# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8080 (Cloud Run expects this)
EXPOSE 8080

# Run Gunicorn WSGI server on port 8080
CMD exec gunicorn BrillianBengaluru.wsgi:application --bind :8080 --workers 2 --threads 4
