import traceback
from notion_client import Client
from config import constants
from logging_module import logger


class NotionApiClient:
    def __init__(self):
        self.notion = Client(auth=constants.NOTION_API_TOKEN)

    async def get_team_contact_list(self):
        try:
            response = self.notion.databases.query(
                database_id=constants.NOTION_TEAM_CONTACT_PAGE_DATABASE_ID
            )
            return {"status_code": 200, "data": response}
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error in get_team_contact_list: {e}")
            return {"status_code": 500, "data": f"Error in get_team_contact_list: {e}"}
