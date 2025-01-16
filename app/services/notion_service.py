from thirdparty.notion_api_service import NotionApiClient
from logging_module import logger


async def get_formatted_team_contacts():
    try:
        notion_client = NotionApiClient()
        response = await notion_client.get_team_contact_list()
        if response["status_code"] != 200:
            return response
        data = response["data"]
        team_contact_list = []
        for item in data["results"]:
            source = item["properties"]
            if not source["Email"]["email"]:
                continue
            team_contact_list.append(
                {
                    "email": source["Email"]["email"],
                    "location": [
                        location["name"]
                        for location in source["Location"]["multi_select"]
                    ],
                    "department": [
                        department["name"]
                        for department in source["Department"]["multi_select"]
                    ],
                }
            )
        return {"status_code": 200, "data": team_contact_list}
    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.error(f"Error in get_formatted_team_contacts: {e}")
        return {
            "status_code": 500,
            "data": f"Error in get_formatted_team_contacts: {e}",
        }
