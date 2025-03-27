from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.conversations import Conversation
from models.message import Message

message_bp = Blueprint("message", __name__)

@message_bp.route("/", methods=["POST"])
@jwt_required()
def create_message():
    user_id = get_jwt_identity()
    data = request.get_json()

    conversation_id = data.get("conversation_id")
    content = data.get("content")

    if not all([conversation_id, content]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Verify the conversation belongs to the user
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404
    
    # Stores user message
    message = Message(conversation_id=conversation_id, role="user", content=content)
    db.session.add(message)

    # Update conversation timestamp
    conversation.updated_at = db.func.now()
    db.session.commit()

    return jsonify({
        "message": "Message created successfully",
        "data": message.to_dict()
    }), 201

@message_bp.route("/assistant", methods=["POST"])
@jwt_required()
def create_assistant_message():
    """Endpoint for storing assistant messages (used by the Tornado server)"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    conversation_id = data.get("conversation_id")
    content = data.get("content")

    if not all([conversation_id, content]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Verify the conversation belongs to the user
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404
    
    # Stores assistant message
    message = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=content
    )
    db.session.add(message)

    # Update conversation timestamp
    conversation.updated_at = db.func.now()
    db.session.commit()

    return jsonify({
        "message": "Assistant message created successfully",
        "data": message.to_dict()
    }), 201