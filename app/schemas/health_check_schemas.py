

openai_health_check_response_schema = {
        200: {
            "description": "OpenAI service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "response": "OpenAI is operational",
                        "finish_reason": "stop",
                        "token_usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
                        "status_code": 200
                    }
                }
            }
        },
        500: {
            "description": "Error in OpenAI service",
            "content": {
                "application/json": {
                    "example": {
                        "response": "Error connecting to OpenAI",
                        "status_code": 500
                    }
                }
            }
        },
    }