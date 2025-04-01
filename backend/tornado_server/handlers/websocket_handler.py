import json
import logging
import asyncio
import uuid
from datetime import datetime
from tornado.websocket import WebSocketHandler
from tornado.escape import json_decode, json_encode

from services.llm_service import LLMService
from services.auth_service import validate_jwt_token
from services.message_service import MessageService
from utils.logging_utils import setup_request_logger

logger = logging.getLogger(__name__)

class ChatWebSocketHandler(WebSocketHandler):
    """WebSocket handler for chat interactions."""

    connections = set()

    def initialize(self):
        """Initialize the handler."""
        self.user_id = None
        self.conversation_id = None
        self.llm_service = LLMService()
        self.message_service = MessageService()
        self.request_logger = setup_request_logger()

    def check_origin(self, origin):
        """Allow connections from any origin."""
        # In production, you should restrict this to your allowed origins
        return True

    async def open(self):
        """Handler new WebSocket connections."""
        self.request_logger.info("New WebSocket connection opened")
        ChatWebSocketHandler.connections.add(self)

    async def on_message(self, message):
        """Handle incoming messages from clients."""
        try:
            message_data = json_decode(message)

            # Process message based on type
            msg_type = message_data.get("type", "")

            if msg_type == "auth":
                await self.handle_auth(message_data)
            elif msg_type == "prompt":
                await self.handle_prompt(message_data)
            elif msg_type == "create_conversation":
                await self.handle_create_conversation(message_data)
            elif msg_type == "select_conversation":
                await self.handle_select_conversation(message_data)
            else:
                await self.send_error("Unknown message type")
        
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON message")
        except Exception as e:
            self.request_logger.exception("Error processing message: {e}")
            await self.send_error(f"Internal server error: {str(e)}")

    async def handle_auth(self, data):
        """Handle authentication message."""
        token = data.get("token")
        if not token:
            await self.send_error("No authentication token")
            return
        
        # Validate JWT token
        user_id = await validate_jwt_token(token)
        if not user_id:
            await self.send_error("Invalid authentication token")
            return

        self.user_id = user_id
        self.request_logger.info(f"User {user_id} authenticated via WebSocket")

        await self.write_message(json_encode({
            "type": "auth_success",
            "user_id": user_id
        }))

    async def hanlde_create_conversation(self, data):
        """Handle creation of a new conversation."""
        if not self.user_id:
            await self.send_error("Authentication required")
            return
        
        title = data.get("title", f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Create a conversation via the Flask API
        conversation = await self.message_service.create_conversation(self.user_id, title)

        if not conversation:
            await self.send_error("Failed to create conversation")
            return
        
        self.conversation_id = conversation.get('id')
        await self.write_message(json_encode({
            "type": "conversation_created",
            "conversation": conversation
        }))

    async def handle_select_conversation(self, data):
        """Handle selection of an existing conversation."""
        if not self.user_id:
            await self.send_error("Authentication required")
            return

        conversation_id = data.get('conversation_id')
        if not conversation_id:
            await self.send_error("No conversation ID provided")
            return
        
        # Verify the conversation exists and belongs to the user
        conversation = await self.message_service.get_conversation(self.user_id, conversation_id)

        if not conversation:
            await self.send_error("Conversation not found")
            return
        
        self.conversation_id = conversation_id

        await self.write_message(json_encode({
            "type": "conversation_selected",
            "conversation": conversation
        }))

    async def handle_prompt(self, data):
        """Handle user prompt and stream LLM response."""
        if not self.user_id:
            await self.send_error("Authentication required")
            return
        
        if not self.conversation_id:
            # Auto-create a conversation if needed
            await self.hanlde_create_conversation({})
        
        prompt = data.get('prompt')
        if not prompt:
            await self.send_error("No prompt provided")
            return
        
        # Save user message
        await self.message_service.save_message(self.conversation_id, 'user', prompt)

        # Prepare response message
        response_message_id = str(uuid.uuid4())
        await self.write_message(json_encode({
            "type": "assistant_response_start",
            "message_id": response_message_id
        }))

        # Variable to collect the full response
        full_response = ""

        # Stream the LLM response
        try:
            async for token in self.llm_service.stream_completion(prompt):
                full_response += token

                await self.write_message(json_encode({
                    "type": "assistant_response_chunk",
                    "message_id": response_message_id,
                    "chunk": token
                }))

                # Small delay to prevent overwhelming the client
                await asyncio.sleep(0.01)
        
        except Exception as e:
            self.request_logger.exception(f"Error streaming LLM response: {e}")
            await self.send_error(f"Error generating response: {str(e)}")
            return
        
        # Signal end of response
        await self.write_message(json_encode({
            "type": "assistant_response_end",
            "message_id": response_message_id,
        }))

        # Save the assistant's message
        await self.message_service.save_message(self.conversation_id, 'assistant', full_response)

        self.request_logger.info(f"LLM response completed for conversation {self.conversation_id}")

    async def send_error(self, message):
        """Send an error message to the client."""
        await self.write_message(json_encode({
            "type": "error",
            "message": message
        }))

    def on_close(self):
        """Handle WebSocket connection close."""
        ChatWebSocketHandler.connections.remove(self)
        self.request_logger.info("WebSocket connection closed")

    