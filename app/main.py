import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    email_agent_router,
    user_router,
    health_check_router,
    pinecone_router,
    train_agent_router,
    client_agent_training_controller,
    service_titan_router,
    slack_router,
    vonage_router,
    notion_router,
    gmail_router
)
import services
from fastapi_utils.tasks import repeat_every
from config import constants

@repeat_every(seconds=3600)
async def service_titan_customers_sync():
    try:
        print("Running service_titan_customers_sync")
        await services.export_all_customers_data_from_service_titan()
    except Exception as e:
        print(f"Error in service_titan_customers_sync: {e}")

async def startup_lifespan():
    if constants.DEBUG:
        return
    print("Running startup_lifespan")
    await services.generate_index_service()
    await service_titan_customers_sync()
    print("Finished startup_lifespan")

project = FastAPI(on_startup=[startup_lifespan])

static_dir = "static"

if not os.path.isdir(static_dir):
    os.makedirs(static_dir)

project.mount("/static", StaticFiles(directory=static_dir), name=static_dir)

project.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@project.get("/", tags=["Health Check"])
async def health_check():
    return {"message": "Welcome to TouchStone Electric Chatbot Docs!!"}


# Include routers
project.include_router(gmail_router.router, prefix="/api", tags=["Gmail"])
project.include_router(email_agent_router.router, prefix="/api", tags=["Email Agent"])
project.include_router(user_router.router, prefix="/api", tags=["User"])
project.include_router(health_check_router.router, prefix="/api", tags=["Health Check"])
project.include_router(pinecone_router.router, prefix="/api", tags=["Pinecone"])
project.include_router(train_agent_router.router, prefix="/api", tags=["Train Agent"])
project.include_router(client_agent_training_controller.router, prefix="/api", tags=["Client Agent Training"])
project.include_router(service_titan_router.router, prefix="/api", tags=["Service Titan"])
project.include_router(slack_router.router, prefix="/api", tags=["Slack"])
project.include_router(vonage_router.router, prefix="/api", tags=["Vonage"])
project.include_router(notion_router.router, prefix="/api", tags=["Notion"])





