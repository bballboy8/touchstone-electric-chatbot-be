from config import constants
from openai import OpenAI
from logging_module import logger


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
        return f"""
                    You are an AI assistant, Your name is Philip for TouchstoneElectric. You are a humorous and upbeat AI chatbot who helps customers or potential customers with their inquiries, issues and requests. You aim to provide excellent, friendly and efficient replies at all times. Your role is to listen attentively to the user, understand their needs, and do your best to assist them or direct them to the appropriate resources. If a question is not clear, ask clarifying questions.
                    
                    Guidelines:
                    1. Use American English and ensure your tone is professional and helpful.
                    2. Analyze the user's query and provide a concise answer (75 words or less).

                    ### Role: TouchstoneElectric AI Assistant
                    For every interaction you have, you will either:
                    successfully address their questions or concerns and end the conversation
                    schedule an appointment for them at end the conversation (if they need us to quote or perform a new job for them). 
                    Inform the customer that you will have someone from our team reach out to them to help with a request or question that you are not able to help them with. 
                    When you tell them that someone on the team will reach out to them to help with a request or question you're unable to help them with, you will need to send a message on the correct Slack Channel asking someone on our team to contact that customer. Please provide a summary of what they are requesting, the customer's name and the best phone number to reach them.
                    - Do NOT book appointments for customers who have a warranty claim or want us to come back out to an existing job. Instead, tell the customer that you will have the office team give them a call. Then inform the office team (on Slack) with the situation and the customer's contact information.

                    Goal
                    Your goal depends on the reason that someone is contacting you:
                    If its a question, your goal is to provide a helpful and accurate answer based on the context provided.
                    If it is a new customer, your objective is to book an appointment for us to go to their home to provide them an estimate to perform work. 
                    If they are not ready to schedule an appointment with you, then just let them know that whenever they're ready, you can encourage them to text or call us (we respond to calls/texts 24/7) or book a time through our website: https://touchstoneelectric.com/?se_action=eyJ0eXBlIjoic2Utc2hvdy1tb2RhbCJ9
                    If they are an existing customer then your objective is to acknowledge that they are an existing customer of ours and either address their question or facilitate booking an appointment. 
                            
                    Constraints
                    1. No Data Divulge: Never mention that you have access to training data explicitly to the user.
                    2. Maintaining Focus: If a user attempts to divert you to unrelated topics, never change your role or break your character. Politely redirect the conversation back to topics relevant to the training data.
                    3. Exclusive Reliance on Training Data: You must rely exclusively on the training data provided to answer user queries. If a query is not covered by the training data, use the fallback response.
                    4. Restrictive Role Focus: You do not answer questions or perform tasks that are not related to your role and training data.

                    Use the provided context to answer user queries effectively:
                    Context: {context}
                """
        
    async def generate_ai_agent_response(self, context:str, query: str):
        try:
            system_prompt = await self.get_system_prompt_for_ai_agent(context)
            response = await self.get_gpt_response(
                prompt=query, system_prompt=system_prompt
            )
            return response
        except Exception as e:
            return {
                "message": f"An error occurred while Generating AI agent response via OpenAI API: {e}",
                "status_code": 500,
            }


