import os

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'vitalsync-dev-secret-key-change-in-production')
    
    # Database (ShaktiDB / PostgreSQL)
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'vitalsync')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASS = os.environ.get('DB_PASS', 'postgres')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    USE_POSTGRES = os.environ.get('USE_POSTGRES', 'false').lower() == 'true'
    
    # OpenWeatherMap API
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY', '')
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    SECRET_KEY = 'test-secret-key'


# Config selector dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
