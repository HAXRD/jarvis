from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

from extensions import db
from models.user import User
from models.preference import UserPreference
from utils.validators import validate_email, validate_password

user_bp = Blueprint("user", __name__)

@user_bp.route("/preferences", methods=["GET"])
@jwt_required()
def get_preferences():
    user_id = get_jwt_identity()
    preferences = UserPreference.query.filter_by(user_id=user_id).first()

    if not preferences:
        # Create default preferences if not exist
        preferences = UserPreference(user_id=user_id)
        db.session.add(preferences)
        db.session.commit()
    
    return jsonify({
        "preferences": preferences.to_dict()
    }), 200

@user_bp.route("/preferences", methods=["PUT"])
@jwt_required()
def update_preferences():
    user_id = get_jwt_identity()
    data = request.get_json()

    preferences = UserPreference.query.filter_by(user_id=user_id).first()

    if not preferences:
        preferences = UserPreference(user_id=user_id)
        db.session.add(preferences)
    
    if "theme" in data:
        preferences.theme = data["theme"]

    if "model_preference" in data:
        preferences.model_preference = data["model_preference"]
    
    db.session.commit()

    return jsonify({
        "message": "Preferences updated!",
        "preferences": preferences.to_dict()
    }), 200

@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404
    
    data = request.get_json()
    
    if "username" in data and data["username"] != user.username:
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({
                "error": "Username already exists"
            }), 409
        user.username = data["username"]
        
    if "email" in data and data["email"] != user.email:
        if not validate_email(data["email"]):
            return jsonify({
                "error": "Invalid email format"
            }), 400
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({
                "error": "Email already in use"
            }), 409
        user.email = data["email"]
        
        
    if "password" in data:
        if not validate_password(data["password"]):
            return jsonify({
                "error": "Password must be at least 8 characters long and contain letters and numbers"
            }), 400
        user.password_hash = generate_password_hash(data["password"])
    
    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "user": user.to_dict()
    }), 200
