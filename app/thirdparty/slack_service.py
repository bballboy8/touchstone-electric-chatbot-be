from slack_sdk import WebClient
from config import constants
from slack_sdk.errors import SlackApiError
from services.train_agent_service import query_via_ai_agent
from logging_module import logger


class SlackServiceAPI:
    def __init__(self):
        self.slack_client = WebClient(token=constants.SLACK_BOT_TOKEN)

    async def send_message(self, channel, message):
        response = self.slack_client.chat_postMessage(
            channel=channel,
            text=message,
        )
        return response

    # handle slack events
    async def handle_event(self, content_type, data):
        logger.debug(f"Content-Type: {content_type}")

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

                bot_response = await query_via_ai_agent(user_message)

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
                bot_response = await query_via_ai_agent(user_message)

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
