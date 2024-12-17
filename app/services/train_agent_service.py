import pdfplumber
from nltk.tokenize import sent_tokenize
import os
from logging_module import logger
from services import PineConeDBService, OpenAIService
from services.client_agent_training_service import get_current_knowledge_books_service
from fastapi import UploadFile, File
import re
import json
import uuid


async def extract_useful_pages(pdf_path, min_words=20, skip_keywords=None):
    try:
        useful_pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text_simple()
                if not text:
                    continue

                useful_pages.append({"page_number": i + 1, "text": text})
        return {"status_code": 200, "response": useful_pages}
    except Exception as e:
        return {
            "status_code": 500,
            "response": f"Error while extracting useful pages: {e}",
        }


async def chunk_text(text, max_tokens=900):
    try:
        # sentences = sent_tokenize(text)
        # chunks = []
        # current_chunk = []
        # current_length = 0

        # for sentence in sentences:
        #     sentence_length = len(sentence.split())
        #     if current_length + sentence_length > max_tokens:
        #         chunks.append(" ".join(current_chunk))
        #         current_chunk = []
        #         current_length = 0
        #     current_chunk.append(sentence)
        #     current_length += sentence_length

        # if current_chunk:
        #     chunks.append(" ".join(current_chunk))
        return {"status_code": 200, "response": [text]}
    except Exception as e:
        return {"status_code": 500, "response": f"Error while chunking text: {e}"}


async def store_embeddings_in_pinecone(chunks, knowledge_book_name=None):
    try:
        pinecone_client = PineConeDBService()
        openai_client = OpenAIService()
        cooked_chunks = []
        temp_debug_list = []
        for i, chunk in enumerate(chunks):
            openai_response = await openai_client.generate_text_embeddings(
                chunk["text"]
            )
            temp_debug_list.append(openai_response)
            embedding = openai_response["embedding"]
            metadata = {"page_number": chunk["page_number"], "text": chunk["text"]}
            unique_id = str(uuid.uuid4())
            cooked_chunks.append((f"chunk-{i}-{unique_id}", embedding, metadata))
        pinecone_response = await pinecone_client.populate_cooked_records(cooked_chunks, knowledge_book_name)

        return {
            "status_code": 200,
            "response": len(cooked_chunks),
            "message": pinecone_response["response"],
        }
    except Exception as e:
        return {"status_code": 500, "response": f"Error while storing embeddings: {e}"}


def clean_newlines(text):
    return text


async def upload_pdf_for_training_agent(file: UploadFile = File(...), knowledge_book_name: str = None):    
    # Save uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    try:
        
        if knowledge_book_name:
            response = await get_current_knowledge_books_service()
            if response["status_code"] != 200:
                return response
            
            if knowledge_book_name not in response["response"]:
                return {
                    "status_code": 400,
                    "response": f"Knowledge Book '{knowledge_book_name}' does not exist.",
                }


        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        # Process the PDF
        useful_pages = await extract_useful_pages(temp_file_path)
        if useful_pages["status_code"] != 200:
            return useful_pages

        logger.debug("Useful Pages extracted")
        # Chunk and embed
        all_chunks = []
        for page in useful_pages["response"]:
            page_chunks = await chunk_text(page["text"])
            if page_chunks["status_code"] != 200:
                continue
            for chunk in page_chunks["response"]:
                text_chunk = clean_newlines(chunk)
                all_chunks.append(
                    {"page_number": page["page_number"], "text": text_chunk}
                )
        num_chunks = await store_embeddings_in_pinecone(all_chunks, knowledge_book_name)
        os.remove(temp_file_path)

        if num_chunks["status_code"] != 200:
            return num_chunks

        return {
            "message": f"PDF processed successfully. {num_chunks['response']} chunks stored in Pinecone. {num_chunks['message']}",
            "useful_pages": useful_pages["response"],
            "all_chunks": all_chunks,
            "status_code": 200,
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {"status_code": 500, "message": f"Error while training agent: {e}"}


async def query_via_ai_agent(query: str, knowledge_book_name: str = None):
    try:
        pinecone_client = PineConeDBService()
        openai_client = OpenAIService()

        if knowledge_book_name:
            response = await get_current_knowledge_books_service()
            if response["status_code"] != 200:
                return response
            
            if knowledge_book_name not in response["response"]:
                return {
                    "status_code": 400,
                    "response": f"Knowledge Book '{knowledge_book_name}' does not exist.",
                }
            

        response = await pinecone_client.query_data(query, 3, knowledge_book_name)
        if response["status_code"] != 200:
            return response

        matches = response["response"]["matches"]

        context = " ".join([match["metadata"]["text"] for match in matches])
        response = await openai_client.generate_ai_agent_response(
            context=context, query=query
        )
        if response["status_code"] != 200:
            return response
        return {
            "message": "Agent query processes successfully",
            "query": query,
            "response": response["response"],
            "status_code": 200,
        }
    except Exception as e:
        return {"status_code": 500, "response": f"Error while querying the agent: {e}"}
