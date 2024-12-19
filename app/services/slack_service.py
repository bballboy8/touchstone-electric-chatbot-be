from thirdparty.slack_service import SlackServiceAPI
from logging_module import logger
from fastapi import HTTPException
import hmac
import hashlib
import time
from config import constants



async def verify_slack_request(body, headers, signing_secret: str):
    timestamp = headers.get("x-slack-request-timestamp")
    slack_signature = headers.get("x-slack-signature")

    if abs(time.time() - int(timestamp)) > 300:
        raise HTTPException(status_code=400, detail="Request is too old.")

    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    computed_signature = (
        "v0="
        + hmac.new(
            signing_secret.encode(), sig_basestring.encode(), hashlib.sha256
        ).hexdigest()
    )

    if not hmac.compare_digest(computed_signature, slack_signature):
        raise HTTPException(status_code=403, detail="Invalid request signature.")


async def slack_events_handler(data, body, headers):
    logger.debug("Inside Slack events handler controller")
    try:
        content_type = headers.get("content-type")
        await verify_slack_request(
            body, headers, signing_secret=constants.SLACK_SIGNING_SECRET
        )
        slack_instance = SlackServiceAPI()
        response = await slack_instance.handle_event(
            content_type=content_type, data=data, headers=headers
        )
        logger.debug("Response from Slack events handler controller")
        return response
    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.error(f"Error in slack_events_handler: {str(e)}")
        return {"status": "error", "message": str(e)}

