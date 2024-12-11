FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"


# Build arguments for environment variables
ARG OPENAI_API_KEY
ARG PINECONEDB_API_KEY
ARG SERVICE_TITAN_TENANT_ID
ARG SERVICE_TITAN_CLIENT_ID
ARG SERVICE_TITAN_CLIENT_SECRET
ARG SERVICE_TITAN_BASE_AUTH_URL
ARG SERVICE_TITAN_BASE_API_URL
ARG SERVICE_TITAN_APP_KEY

# Pass the arguments to environment variables
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV PINECONEDB_API_KEY=$PINECONEDB_API_KEY
ENV SERVICE_TITAN_TENANT_ID=$SERVICE_TITAN_TENANT_ID
ENV SERVICE_TITAN_CLIENT_ID=$SERVICE_TITAN_CLIENT_ID
ENV SERVICE_TITAN_CLIENT_SECRET=$SERVICE_TITAN_CLIENT_SECRET
ENV SERVICE_TITAN_BASE_AUTH_URL=$SERVICE_TITAN_BASE_AUTH_URL
ENV SERVICE_TITAN_BASE_API_URL=$SERVICE_TITAN_BASE_API_URL
ENV SERVICE_TITAN_APP_KEY=$SERVICE_TITAN_APP_KEY

# Add the current working directory to PYTHONPATH
ENV PYTHONPATH=/app/app

# Expose the default port for the application
EXPOSE 8080

# Run the FastAPI application
CMD ["uvicorn", "main:project", "--host", "0.0.0.0", "--port", "8080"]
