from fastapi import APIRouter, UploadFile, File
import services
from logging_module import logger


router = APIRouter()


@router.post(
    "/train-agent-via-pdf",
)
async def train_agent_via_pdf(training_pdf: UploadFile = File(...)):
    logger.debug("Inside Train Agent Via Pdf controller")
    response = await services.upload_pdf_for_training_agent(file=training_pdf)
    logger.debug("Response from Generate Embedding using pinecone controller")
    return response

@router.post(
    "/query-agent",
)
async def query_agent(query: str):
    logger.debug("Inside Query Agent controller")
    response = await services.query_via_ai_agent(query)
    logger.debug("Response from Query Agent controller")
    return response