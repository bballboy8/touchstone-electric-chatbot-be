from config import constants
from openai import OpenAI
from logging_module import logger
import os
from fastapi import UploadFile, File


class OpenAIService:
    def __init__(self):
        """
        Initialize the OpenAI service with the API key from the constants file.
        """
        self.openai_client = OpenAI(
            api_key=constants.OPENAI_API_KEY,
        )

    async def get_gpt_response(self, prompt: str, system_prompt: str) -> dict:
        """
        Send the prompt to the GPT API asynchronously and return the response.

        Args:
            prompt (str): The user's input prompt for the GPT model.
            system_prompt (str): The system prompt that sets the context or behavior for GPT.

        Returns:
            dict: A dictionary containing the GPT response, finish reason, token usage, and status code.
            Keys:
                - response (str): The GPT model's response.
                - finish_reason (str): The reason why the generation ended (e.g., 'stop', 'length').
                - prompt_tokens (int): Number of tokens in the input prompt.
                - completion_tokens (int): Number of tokens in the generated response.
                - status_code (int): HTTP-like status code (200 for success, 500 for error).
        """
        try:
            logger.info("Sending prompt to OpenAI GPT API...")
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            )
            if "errors" in response:
                logger.error(
                    f"An error occurred while processing the request: {response['errors']}"
                )
                return {
                    "response": f"An error occurred while processing the request: {response['errors']}",
                    "status_code": 500,
                }
            finish_reason = response.choices[0].finish_reason
            response_data = response.choices[0].message.content
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            return {
                "response": response_data,
                "finish_reason": finish_reason,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "status_code": 200,
            }
        except Exception as e:
            logger.error(f"An error occurred while processing the request: {e}")
            return {
                "response": f"An error occurred while processing the request: {e}",
                "status_code": 500,
            }

    async def test_openai_for_chat_completion(self):
        """
        Test the GPT API for Chat Completion asynchronously by sending a sample prompt.

        Returns:
            str: A formatted string containing the GPT model's response, reason for completion,
            and token usage, or an error message if the request fails.
        """
        try:
            prompt = "Hi there! How are you doing today?"
            system_prompt = "You are an expert conversationalist. Please respond to the user's message with a friendly greeting."
            response = await self.get_gpt_response(prompt, system_prompt)
            if response["status_code"] == 500:
                return response

            message = (
                f"Response from Model: {response['response']}\n"
                f"Reason for completion: {response['finish_reason']}\n"
                f"Prompt tokens: {response['prompt_tokens']}\n"
                f"Completion tokens: {response['completion_tokens']}"
            )
            return {"message": message, "status_code": 200}
        except Exception as e:
            logger.error(f"An error occurred while testing the OpenAI API: {e}")
            return {
                "message": f"An error occurred while testing the OpenAI API: {e}",
                "status_code": 500,
            }

    async def generate_text_embeddings(self, text):
        try:
            embedding_model = constants.EMBEDDING_MODEL
            response = self.openai_client.embeddings.create(
                input=text,
                model=embedding_model
            )
            return {"status_code": 200 , "embedding": response.data[0].embedding}
        except Exception as e:
            logger.error(f"An error occurred while Generating the embeddings via API: {e}")
            return {
                "message": f"An error occurred while Generating the embeddings via OpenAI API: {e}",
                "status_code": 500,
            }

    async def get_system_prompt_for_ai_agent(self, context: str):
        try:
            if not os.path.exists("prompt.txt"):
                with open("prompt.txt", "w") as file:
                    file.write("Be professional and courteous in your responses.")

            with open("prompt.txt", "r") as file:
                prompt_template = file.read()
                prompt_template += f"""
                    Use the provided context to answer user queries effectively:
                    Context: {context}
                """
            prompt_template= "You works for Touchstone Electric. " + prompt_template
            return {"status_code": 200, "system_prompt": prompt_template}
        except Exception as e:
            return {
                "message": f"An error occurred while getting system prompt for AI agent: {e}",
                "status_code": 500,
            }

    async def generate_ai_agent_response(self, context:str, query: str):
        try:
            system_prompt = await self.get_system_prompt_for_ai_agent(context)
            if system_prompt.get("status_code") != 200:
                return system_prompt

            system_prompt = system_prompt.get("system_prompt")

            response = await self.get_gpt_response(
                prompt=query, system_prompt=system_prompt
            )
            return response
        except Exception as e:
            return {
                "message": f"An error occurred while Generating AI agent response via OpenAI API: {e}",
                "status_code": 500,
            }

    async def update_system_prompt(self, system_prompt: str):
        try:
            with open("prompt.txt", 'w') as file:
                file.write(system_prompt)

            return {"status_code": 200, "message": "System prompt updated successfully."}
        except Exception as e:
            return {
                "message": f"An error occurred while updating system prompt: {e}",
                "status_code": 500,
            }

    async def extract_user_details(self, user_query: str, previous_messages: list):
        try:
            system_prompt = """ 
                            Extract the user's details (name, email, phone number, address, visit date and time) from the given query and messages. 
                            Return only valid JSON in the following RFC8259-compliant format, and do not include any extra text or explanations outside the JSON object:
                            {
                                "name": "John Doe",
                                "email": "email@email.com",
                                "phone": "1234567890",
                                "address": "123, Street Name, City, Country",
                                "start": "2022-01-01T00:00:00Z"
                            }
                            Ensure:
                            1. If any field is missing, use an empty string "" for that field value.
                            """

            response = await self.get_gpt_response_with_history(
                prompt=user_query, system_prompt=system_prompt, previous_messages=previous_messages
            )
            return response
        except Exception as e:
            return {
                "message": f"An error occurred while extracting user details: {e}",
                "status_code": 500,
            }
        
    async def extract_user_basic_details(self, user_query: str, previous_messages: list):
        try:
            system_prompt = """ 
                            Extract the user's details (name, phone number, address) from the given query and messages. 
                            Return only valid JSON in the following RFC8259-compliant format, and do not include any extra text or explanations outside the JSON object:
                            {
                                "name": "John Doe",
                                "phone": "1234567890",
                                "address": "123, Street Name, City, Country"
                            }
                            Ensure:
                            1. If any field is missing, use an empty string "" for that field value.
                            """

            response = await self.get_gpt_response_with_history(
                prompt=user_query, system_prompt=system_prompt, previous_messages=previous_messages
            )
            return response
        except Exception as e:
            return {
                "message": f"An error occurred while extracting user details: {e}",
                "status_code": 500,
            }

    async def generate_ai_agent_response_with_history(
        self, context: str, query: str, previous_messages: list
    ):
        try:
            system_prompt = await self.get_system_prompt_for_ai_agent(context)
            if system_prompt.get("status_code") != 200:
                return system_prompt

            system_prompt = system_prompt.get("system_prompt")

            response = await self.get_gpt_response_with_history(
                prompt=query,
                system_prompt=system_prompt,
                previous_messages=previous_messages,
            )
            return response
        except Exception as e:
            return {
                "message": f"An error occurred while Generating AI agent response via OpenAI API: {e}",
                "status_code": 500,
            }

    async def get_gpt_response_with_history(
        self, prompt: str, previous_messages: list, system_prompt: str
    ) -> dict:
        try:
            logger.info("Sending prompt to OpenAI GPT API...")
            messages = [
                {"role": "system", "content": system_prompt},
            ]
            messages += previous_messages
            messages.append({"role": "user", "content": prompt})



            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            if "errors" in response:
                logger.error(
                    f"An error occurred while processing the request: {response['errors']}"
                )
                return {
                    "response": f"An error occurred while processing the request: {response['errors']}",
                    "status_code": 500,
                }
            finish_reason = response.choices[0].finish_reason
            response_data = response.choices[0].message.content
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            return {
                "response": response_data,
                "finish_reason": finish_reason,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "status_code": 200,
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"An error occurred while processing the request: {e}")
            return {
                "response": f"An error occurred while processing the request: {e}",
                "status_code": 500,
            }

    async def get_conversation_summary(self, conversation: list):
        try:
            system_prompt = """ 
                            Summarize the conversation between the user and the AI agent. 
                            Return a summary of the conversation and reason for visit. You only need to respond with conversation main points no need to include any contact details/address/visit date or time. If email is available please include that. Keep it very concise.
                            """
            response = await self.get_gpt_response_with_history(
                prompt="Generate concise Summary", system_prompt=system_prompt, previous_messages=conversation
            )
            return response
        except Exception as e:
            return {
                "message": f"An error occurred while generating conversation summary: {e}",
                "status_code": 500,
            }
        
    async def get_general_conversation_summary(self, conversation: list):
        try:
            system_prompt = """ 
                            Summarize the conversation between the user and the AI agent. 
                            Return a summary of the conversation. You only need to respond with conversation main points no need to include any contact details/address/visit date or time. If email is available please include that.
                            """
            response = await self.get_gpt_response_with_history(
                prompt="Generate Summary", system_prompt=system_prompt, previous_messages=conversation
            )
            return response
        except Exception as e:
            return {
                "message": f"An error occurred while generating conversation summary: {e}",
                "status_code": 500,
            }