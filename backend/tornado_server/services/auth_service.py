import jwt
import logging
from datetime import datetime, timezone
from config import get_config

logger = logging.getLogger(__name__)
config = get_config()

async def validate_jwt_token(token):
    """
    Validate JWT token and return user_id if valid.

    Args:
        token (str): The JWT token to validate.

    Returns:
        str: The user_id if the token is valid, None otherwise.
    """
    try:
        payload = jwt.decode(
            token, 
            config.JWT_SECRET_KEY,
            algorithms=["HS256"],
            )
        
        # Check if token has expired
        exp = payload.get("exp")
        if exp and datetime.now(timezone.utc).timestamp() > exp:
            logger.warning("Expired JWT token")
            return None
        
        # Return the user_id from the payload
        return payload.get("sub")
    
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {e}")
        return None
    except Exception as e:
        logger.error(f"Error validating JWT token: {e}")
        return None