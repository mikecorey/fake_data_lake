# Use the official lightweight Python image.
FROM python:3.13-slim-bookworm

# Set a working directory.
WORKDIR /app

# Copy requirements.txt and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code to the container.
COPY . .

# Cloud Run requires your application to listen on 0.0.0.0, port 8080.
# Optional: We set an ENV variable for clarity. 
ENV PORT 8080

# Expose the port (not strictly required by Cloud Run, but useful for local testing).
EXPOSE 8080

# Start Gunicorn to serve the Flask app.
# Assuming your Flask instance is named `app` in `app.py`.
CMD exec gunicorn --bind :$PORT app:app