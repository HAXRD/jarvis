import os

class BaseConfig:
    """Base Configuration"""
    DEBUG = False
    FLASK_API_URL = os.environ.get("FLASK_API_URL", "http://127.0.0.1:5001")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt_dev_secret")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    # LLM Service Configuration
    LLM_API_URL = os.environ.get("LLM_API_URL", "https://api.deepseek.com")
    LLM_API_KEY = os.environ.get("LLM_API_KEY", "sk-...")
    LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")
    LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", 0.7))
    LLM_MAX_TOKENS = int(os.environ.get("LLM_MAX_TOKENS", 2048))

class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    DEBUG = True

class ProductionConfig(BaseConfig):
    """Production Configuration"""
    pass

def get_config():
    """Get the configuration based on the environment"""
    env = os.environ.get("CONFIG", "development")

    if env == "development":
        return DevelopmentConfig()
    elif env == "production":
        return ProductionConfig()
    else:
        raise ValueError(f"Invalid configuration: {env}")
    
    