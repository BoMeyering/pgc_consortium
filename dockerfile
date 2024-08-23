# PGC Consortium Django Project Dockerfile
FROM python:3.11-slim

# Set the working directory inside the container
# CHANGE WHERE THIS IS LOCATED
WORKDIR /usr/src/app 

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Expose the port that Django will run on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]