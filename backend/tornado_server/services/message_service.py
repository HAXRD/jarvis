import logging
import aiohttp
import json
from config import get_config

logger = logging.getLogger(__name__)
config = get_config()

class MessageService:
    """Service to interact with Flask API for message storage."""

    def __init__(self):
        """Initialize the message service."""
        self.api_base_url = config.FLASK_API_URL

    async def create_conversation(self, user_id, title):
        """Create a new conversation via Flask API."""
        url = f"{self.api_base_url}/api/conversations/"
        headers = {"Content-Type": "application/json"}

        # Create JWT token for Flask API auth
        payload = {
            "title": title,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=10,
                ) as response:
                    if response.status != 201:
                        error_text = await response.text()
                        logger.error(f"Failed to create conversation: {response.status}, {error_text}")
                        return None
                    
                    response_data = await response.json()
                    return response_data.get("conversation")
        
        except Exception as e:
            logger.exception(f"Error creating conversation: {e}")
            return None
        
    async def get_conversation(self, user_id, conversation_id):
        """Get conversation details from Flask API."""
        url = f"{self.api_base_url}/api/conversations/{conversation_id}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    timeout=10,
                    ) as response:
                    if response.status != 200:
                        if response.status == 404:
                            logger.warning(f"Conversation {conversation_id} not found")
                        else:
                            error_text = await response.text()
                            logger.error(f"Failed to get conversation: {response.status}, {error_text}")
                        return None
                    
                    response_data = await response.json()
                    return response.get('conversation')
        except Exception as e:
            logger.exception(f"Error getting conversation: {e}")
            return None
    
    async def save_message(self, conversation_id, role, content):
        """Save a message to the database via Flask API."""
        if role == "user":
            url = f"{self.api_base_url}/api/messages/"
        else:
            url = f"{self.api_base_url}/api/messages/assistant"

        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "conversation_id": conversation_id,
            "content": content,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=10,
                ) as response:
                    if response.status != 201:
                        error_text = await response.text()
                        logger.error(f"Failed to save message: {response.status}, {error_text}")
                        return False
                    
                    return True
        except Exception as e:
            logger.exception(f"Error saving message: {e}")
            return False