# Use an official Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables (can be overridden at runtime)
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Start the app
CMD ["flask", "run"]