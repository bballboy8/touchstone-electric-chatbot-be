FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Build arguments for environment variables
ARG OPENAI_API_KEY
ARG PINECONEDB_API_KEY

# Pass the arguments to environment variables
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV PINECONEDB_API_KEY=$PINECONEDB_API_KEY

# Add the current working directory to PYTHONPATH
ENV PYTHONPATH=/app/app

# Expose the default port for the application
EXPOSE 8080

# Run the FastAPI application
CMD ["uvicorn", "main:project", "--host", "0.0.0.0", "--port", "8080"]
