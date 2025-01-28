##prospect_app
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()


def app(scope, receive, send):
    ...


if __name__ == "__main__":
    uvicorn.run(
        "main:project",
        host= "localhost" if os.environ.get("DEBUG") == "True" else "0.0.0.0",
        port= int(os.environ.get("PORT", 8010 )) if os.environ.get("DEBUG") == "True" else 8080,
        reload=True,
        log_level="info",
        env_file=".env",
    )
