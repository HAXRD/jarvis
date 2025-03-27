from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def jwt_required_middleware():
    # Skip authentication for these endpoints
    if request.path.startswith("/api/auth/login") or \
    request.path.startswith("/api/auth/register") or \
    request.path.startswith("/api/auth/refresh") or \
    request.path == "/health":
        return
    
    try:
        verify_jwt_in_request()
    except Exception as e:
        if request.path.startswith("/api/"):
            return jsonify({"error": "Authentication required"}), 401
        