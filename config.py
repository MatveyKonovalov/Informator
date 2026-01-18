# config.py
import os
from dataclasses import dataclass

@dataclass
class ServerConfig:
    """Конфигурация сервера"""
    host: str = os.getenv('SERVER_HOST', 'localhost')
    port: int = int(os.getenv('SERVER_PORT', '8000'))
    use_ssl: bool = os.getenv('USE_SSL', 'False').lower() == 'true'
    certfile: str = os.getenv('SSL_CERTFILE', '')
    keyfile: str = os.getenv('SSL_KEYFILE', '')
    
    # Настройки базы данных
    airtable_token: str = os.getenv('AIRTABLE_TOKEN', '')
    airtable_base_id: str = os.getenv('AIRTABLE_BASE_ID', '')
    
    # Настройки логирования
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    log_file: str = os.getenv('LOG_FILE', 'server.log')

@dataclass
class SecurityConfig:
    """Конфигурация безопасности"""
    # CORS настройки
    allowed_origins: list = None
    
    def __post_init__(self):
        if self.allowed_origins is None:
            self.allowed_origins = ['*']

# Создание конфигурации по умолчанию
server_config = ServerConfig()
security_config = SecurityConfig()