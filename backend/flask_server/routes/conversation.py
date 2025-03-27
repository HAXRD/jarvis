from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.conversations import Conversation
from models.message import Message

conversation_bp = Blueprint("conversation", __name__)

@conversation_bp.route("/", methods=["GET"])
@jwt_required()
def get_conversation():
    user_id = get_jwt_identity()
    conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.updated_at.desc()).all()

    return jsonify({
        "conversations": [conv.to_dict() for conv in conversations]
    }), 200

@conversation_bp.route("/<conversation_id>", methods=["GET"])
@jwt_required()
def get_conversation_by_id(conversation_id):
    user_id = get_jwt_identity()
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404
    
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()

    return jsonify({
        "conversation": conversation.to_dict(),
        "messages": [msg.to_dict() for msg in messages]
    }), 200

@conversation_bp.route("/", methods=["POST"])
@jwt_required()
def create_conversation():
    user_id = get_jwt_identity()
    data = request.json
    title = data.get("title", "New Conversation")

    conversation = Conversation(user_id=user_id, title=title)
    db.session.add(conversation)
    db.session.commit()

    return jsonify({
        "message": "Conversation created successfully",
        "conversation": conversation.to_dict()
    }), 201

@conversation_bp.route("/<conversation_id>", methods=["PUT"])
@jwt_required()
def update_conversation(conversation_id):
    user_id = get_jwt_identity()
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()

    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404
    
    data = request.get_json()
    title = data.get("title")

    if title:
        conversation.title = title
        db.session.commit()

    return jsonify({
        "message": "Conversation updated successfully",
        "conversation": conversation.to_dict()
    }), 200

@conversation_bp.route("/<conversation_id>", methods=["DELETE"])
@jwt_required()
def delete_conversation(conversation_id):
    user_id = get_jwt_identity()
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404
    
    db.session.delete(conversation)
    db.session.commit()
    
    return jsonify({
        "message": "Conversation deleted successfully"
    }), 200