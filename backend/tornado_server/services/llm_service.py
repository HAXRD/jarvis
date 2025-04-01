import logging
import asyncio
import json
import aiohttp
from config import get_config

logger = logging.getLogger(__name__)
config = get_config()

class LLMService:
    """Service to interact with LLM"""

    def __init__(self):
        """Initialize the LLM service"""
        self.api_url = config.LLM_API_URL
        self.api_key = config.LLM_API_KEY
        self.model = config.LLM_MODEL
        self.temperature = config.LLM_TEMPERATURE
        self.max_tokens = config.LLM_MAX_TOKENS

    async def stream_completion(self, prompt):
        """
        Stream the completion from the LLM API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        payload = {
           "model": self.model,
           "prompt": prompt,
           "max_tokens": self.max_tokens,
           "temperature": self.temperature,
           "stream" : True
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=60
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"LLM API error: {response.status}, {error_text}")
                        raise Exception(f"LLM API error: {response.error}")
                    
                    # Parse the streaming response
                    # This will be different depending on the LLM provider's API
                    async for line in response.content:
                        line = line.decode("utf-8").strip()
                        if line.startswith("data: "):
                            data = line[6:]
                            if data.startswith("[DONE]"):
                                break
                            try:
                                json_data = json.loads(data)
                                token = json_data.get("choices", [{}])[0].get("text", "")
                                if token:
                                    yield token
                            except json.JSONDecodeError:
                                logger.warning(f"Could not parse LLM response: {data}")
        except asyncio.TimeoutError:
            logger.error("LLM API request timed out")
            raise Exception("Request to LLM service timed out")
        except Exception as e:
            logger.error(f"Error calling LLM API: {e}")
            raise