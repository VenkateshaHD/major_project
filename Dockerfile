# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the backend code and requirements
COPY backend/ /app/backend/

# Install the required packages
# CPU specific PyTorch is specified via extra-index-url
RUN pip install --no-cache-dir -r backend/requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the application
CMD ["python", "backend/main.py"]
