FROM python:3.9

ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/