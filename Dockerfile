FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y ca-certificates
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

# Add the current working directory to PYTHONPATH
ENV PYTHONPATH=/app/app

# Expose the default port for the application
EXPOSE 8080

# Run the FastAPI application
CMD ["uvicorn", "main:project", "--host", "0.0.0.0", "--port", "8080"]
