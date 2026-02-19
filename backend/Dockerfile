FROM python:3.11-slim

WORKDIR /app

# Copy requirements
ADD requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
ADD app.py .
ADD data.json .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Run Flask app
CMD ["python", "app.py"]