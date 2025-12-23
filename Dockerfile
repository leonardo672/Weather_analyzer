# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose optional port (if needed for web interface / dashboards)
# EXPOSE 8000

# Set entrypoint to scheduler (default behavior)
CMD ["python", "scheduler.py"]
