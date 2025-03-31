# Use official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Cloud Run port
EXPOSE 8080

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
