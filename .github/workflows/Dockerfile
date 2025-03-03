FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY load_data.py .
COPY load_mongodb_data.py .
COPY load_all_databases.py .
COPY docker-compose.yml .

# Create volume mount points
VOLUME ["/app/neo4j_data", "/app/mongo_data"]

# Set command to run when container starts
CMD ["python", "load_all_databases.py"]