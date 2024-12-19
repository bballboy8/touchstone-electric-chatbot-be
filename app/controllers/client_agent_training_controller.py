from fastapi import APIRouter, UploadFile, File, Request
import services
from logging_module import logger
from fastapi import Form
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get(
    "/get-knowledge-books-list",
)
async def get_current_knowledge_books():
    logger.debug("Inside Get Current Knowledge Books controller")
    response = await services.get_current_knowledge_books_service()
    logger.debug("Response from Get Current Knowledge Books controller")
    return response


@router.post(
    "/create-knowledge-book",
)
async def create_knowledge_book(knowledge_book_name: str ):
    """
    Creates a knowledge book with the given name.

    Args:
        knowledge_book_name (str): The name of the knowledge book to create. 
                                   This should be a unique and descriptive string.
    Example:
        knowledge_book_name = "my-knowledge-book-1"
    """
    logger.debug("Inside Create Knowledge Book controller")
    response = await services.create_knowledge_book_service(knowledge_book_name)
    logger.debug("Response from Create Knowledge Book controller")
    return response



@router.post(
    "/add-knowldege-to-book-via-pdf",
)
async def train_agent_via_pdf(knowledge_book_name:str, training_pdf: UploadFile = File(...)):
    logger.debug("Inside Train Agent Via Pdf controller")
    response = await services.upload_pdf_for_training_agent(file=training_pdf, knowledge_book_name=knowledge_book_name)
    logger.debug("Response from Generate Embedding using pinecone controller")
    return response

@router.post(
    "/query-agent-via-knowledge-book",
)
async def query_agent_from_knowledge_book(query: str, knowledge_book_name: str):
    logger.debug("Inside Query Agent controller")
    response = await services.query_via_ai_agent(query, knowledge_book_name)
    logger.debug("Response from Query Agent controller")
    return response

@router.delete(
    "/delete-knowledge-book",
)
async def delete_knowledge_book(knowledge_book_name: str):
    """
    Deletes the knowledge book with the given name.

    Args:
        knowledge_book_name (str): The name of the knowledge book to delete.
    Example:
        knowledge_book_name = "my-knowledge-book-1"
    """
    logger.debug("Inside Delete Knowledge Book controller")
    response = await services.delete_knowledge_book_service(knowledge_book_name)
    logger.debug("Response from Delete Knowledge Book controller")
    return response

@router.put(
    "/update-agent-system-prompt",
)
async def update_agent_system_prompt(system_prompt: str = Form(...)):
    logger.debug("Inside Update Agent System Prompt controller")
    response = await services.update_agent_prompt_service(system_prompt)
    logger.debug("Response from Update Agent System Prompt controller")
    return response


@router.get(
    "/get-system-prompt",
)
async def get_system_prompt():
    logger.debug("Inside Get System Prompt controller")
    response = await services.get_system_prompt_for_ai_agent_service("{context}")
    logger.debug("Response from Get System Prompt controller")
    return response


@router.post(
    "/process-tawk-query",
)
async def process_tawk_query(message: str):
    logger.debug("Inside Process Tawk Query controller")
    response = await services.process_tawk_query_service(message)
    logger.debug("Response from Process Tawk Query controller")
    return JSONResponse(content=response, status_code=200)