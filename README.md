# touchstone-electric-chatbot-be

# FastAPI Touchstone Electric Chatbot

This project is built using Python and requires Docker to run. It utilizes UVicorn as the ASGI server.

## Prerequisites

Python 3.12

## Running the Project

Follow these steps to run the project:

## Clone the Repository:

```
git clone https://github.com/bballboy8/touchstone-electric-chatbot-be/tree/production
cd project
```

1. Create virtual environment : virtualenv venv --python=python3.12
2. Install requirements : pip install -r requirements.txt
3. add .env: touch .env
4. Run the application: python app/application.py


## Environment Variables

you should have app/.env file with all environment variable needed or you can set them

NAME: You can set this environment variable to customize the name displayed by the application. By default, it's set to "World".


## Stopping the Application

To stop the running Docker container, you can use the following command:


## Format code
```bash
ruff --output-format=github .  
```