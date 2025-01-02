from slack_sdk import WebClient
from config import constants
from slack_sdk.errors import SlackApiError
from logging_module import logger
import time
from thirdparty.openai_service import OpenAIService

event_id_list = []
event_message_list = {}
class SlackServiceAPI:
    def __init__(self):
        self.slack_client = WebClient(token=constants.SLACK_BOT_TOKEN)

    async def send_message(self, channel, message):
        response = self.slack_client.chat_postMessage(
            channel=channel,
            text=message,
        )
        return response
    
    async def get_slack_channels(self, cursor):
        response = self.slack_client.conversations_list(
            types="private_channel", cursor=cursor
        )
        return response


    # handle slack events
    async def handle_event(self, content_type, data, headers=None):
        logger.debug(f"Content-Type: {content_type}")
        openai_service = OpenAIService()
        if content_type == "application/json":
            logger.debug("Handling JSON payload")
            try:
                slack_event = data
                print(slack_event)
                    
                if "challenge" in slack_event:
                    return {"challenge": slack_event["challenge"]}

                # Handle message events
                user_message = slack_event["event"]["text"]
                channel_id = slack_event["event"]["channel"]
                user_id = slack_event["event"]["user"]
                event_type = slack_event["event"]["type"]
                event_id = slack_event["event_id"]

                if event_type != "app_mention":
                    return {"status": "ok"}
                
                if event_id in event_id_list:
                    if len(event_id_list) > 10:
                        event_id_list.pop(0)
                    return {"status": "ok"}

                event_id_list.append(event_id)

                # Check if the message is repeated under 10 seconds
                if event_message_list.get(user_id) == user_message:
                    if (time.time() - event_message_list.get(user_id + "_time")) <= 10:
                        if len(event_message_list) > 10:
                            event_message_list.pop(0)
                        return {"status": "ok"}
                event_message_list[user_id] = user_message
                event_message_list[user_id + "_time"] = time.time()

                bot_response = await openai_service

                if bot_response["status_code"] == 500:
                    bot_response = (
                        "I'm sorry, I'm down right now. Please try again later."
                    )
                else:
                    bot_response = bot_response["response"]

                # Send response back to Slack
                try:
                    self.slack_client.chat_postMessage(
                        channel=channel_id, text=f"<@{user_id}> {bot_response} Event: {event_type} Event ID: {event_id}"
                    )
                except SlackApiError as e:
                    print(f"Error sending message: {e.response['error']}")

            except Exception as e:
                import traceback
                traceback.print_exc()
                logger.error(f"Error handling JSON payload: {e}")
                return {"message": str(e), "status_code": 500}

        elif content_type == "application/x-www-form-urlencoded":
            logger.debug("Handling form data")
            try:
                form_data = data
                slack_event = dict(form_data)
                print(slack_event)

                if "challenge" in slack_event:
                    return {"challenge": slack_event["challenge"]}

                # Handle message events
                user_message = slack_event["text"]
                channel_id = slack_event["channel_id"]
                user_id = slack_event["user_id"]

                # Generate AI Response
                bot_response = {"status_code": 200, "response": "Hello"}

                if bot_response["status_code"] == 500:
                    bot_response = (
                        "I'm sorry, I'm down right now. Please try again later."
                    )
                else:
                    bot_response = bot_response["response"]

                # Send response back to Slack
                try:
                    self.slack_client.chat_postMessage(
                        channel=channel_id, text=f"<@{user_id}> {bot_response}"
                    )
                except SlackApiError as e:
                    print(f"Error sending message: {e.response['error']}")

            except Exception as e:
                import traceback
                logger.error(f"Error handling form data: {e}")
                return {"message": str(e), "status_code": 500}
