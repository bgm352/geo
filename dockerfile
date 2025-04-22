FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8050

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
