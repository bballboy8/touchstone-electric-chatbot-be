import pdfplumber
from nltk.tokenize import sent_tokenize
import os
from logging_module import logger
from services import PineConeDBService, OpenAIService
from fastapi import UploadFile, File
import re
import json

async def extract_useful_pages(pdf_path, min_words=50, skip_keywords=None):
    try:
        if skip_keywords is None:
            skip_keywords = ["Index", "Table of Contents", "Training Manual"]

        useful_pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue

                word_count = len(text.split())
                if word_count < min_words:
                    continue  # Skip short pages

                # Check for skip keywords
                if any(keyword in text for keyword in skip_keywords):
                    continue

                # Add page to useful pages
                useful_pages.append({"page_number": i + 1, "text": text})
        return {"status_code": 200, "response": useful_pages}
    except Exception as e:
        return {
            "status_code": 500,
            "response": f"Error while extracting useful pages: {e}",
        }


async def chunk_text(text, max_tokens=900):
    try:
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence.split())
            if current_length + sentence_length > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(sentence)
            current_length += sentence_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return {"status_code": 200, "response": chunks}
    except Exception as e:
        return {"status_code": 500, "response": f"Error while chunking text: {e}"}


async def store_embeddings_in_pinecone(chunks):

    try:
        pinecone_client = PineConeDBService()
        openai_client = OpenAIService()
        cooked_chunks = []
        for i, chunk in enumerate(chunks):
            openai_response = await openai_client.generate_text_embeddings(
                chunk["text"]
            )
            embedding = openai_response["embedding"]
            metadata = {"page_number": chunk["page_number"], "text": chunk["text"]}
            cooked_chunks.append((f"chunk-{i}", embedding, metadata))
        pinecone_response = await pinecone_client.populate_cooked_records(cooked_chunks)
        print(pinecone_response, "pinecone response")
        return {
            "status_code": 200,
            "response": len(cooked_chunks),
            "message": pinecone_response["response"],
        }
    except Exception as e:
        return {"status_code": 500, "response": f"Error while storing embeddings: {e}"}


def clean_newlines(text):
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text


async def upload_pdf_for_training_agent(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    try:
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
        num_chunks = await store_embeddings_in_pinecone(all_chunks)
        os.remove(temp_file_path)

        if num_chunks["status_code"] != 200:
            return num_chunks

        return {
            "message": f"PDF processed successfully. {num_chunks['response']} chunks stored in Pinecone. {num_chunks["message"]}",
            "status_code": 200,
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {"status_code": 500, "message": f"Error while training agent: {e}"}


async def query_via_ai_agent(query: str):
    try:
        pinecone_client = PineConeDBService()
        openai_client = OpenAIService()

        response = await pinecone_client.query_data(query)
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
            "response": response['response'],
            "status_code": 200,
        }
    except Exception as e:
        return {"status_code": 500, "response": f"Error while querying the agent: {e}"}
