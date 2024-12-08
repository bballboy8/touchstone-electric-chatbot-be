import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    user_router,
    health_check_router,
    pinecone_router,
    train_agent_router,
    client_agent_training_controller
)
import services

async def startup_lifespan():
    await services.generate_index_service()


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
project.include_router(user_router.router, prefix="/api", tags=["User"])
project.include_router(health_check_router.router, prefix="/api", tags=["Health Check"])
project.include_router(pinecone_router.router, prefix="/api", tags=["Pinecone"])
project.include_router(train_agent_router.router, prefix="/api", tags=["Train Agent"])
project.include_router(client_agent_training_controller.router, prefix="/api", tags=["Client Agent Training"])



