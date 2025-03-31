# Use Python as the base image (Change if using another language)
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install required Python packages (if applicable)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 8080

# Start the application
CMD ["python", "main.py"]  # Change "main.py" to your actual entry file
