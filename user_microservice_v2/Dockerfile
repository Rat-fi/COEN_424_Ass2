FROM python:3.9-slim

WORKDIR /app

# Copy the shared requirements.txt file from the root context
COPY ../../requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the microservice-specific code
COPY . .

CMD ["python", "user_microservice_v2.py"]  # Update for each service
