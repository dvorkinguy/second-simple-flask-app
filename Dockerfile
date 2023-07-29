# Base image
FROM python:3.9-slim-buster AS base

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Second stage for production
FROM base AS production

# Expose the port your application will be running on
EXPOSE 80

# Set the command to run the application
CMD ["python", "app.py"]

# Third stage for development
FROM base AS development

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0"]