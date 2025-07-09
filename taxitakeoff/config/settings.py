import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application settings and configuration"""
    
    # Default airport code
    default_airport_code: str = "PMI"
    
    # Output directories
    plots_output_dir: str = "output/plots"
    reports_output_dir: str = "output/reports"
    raw_data_dir: str = "data/raw"
    processed_data_dir: str = "data/processed"
    
    # Email configuration (placeholders)
    email_smtp_server: Optional[str] = None
    email_smtp_port: Optional[int] = None
    email_username: Optional[str] = None
    email_password: Optional[str] = None
    email_from: Optional[str] = None
    email_to: Optional[str] = None
    
    # Telegram configuration (placeholders)
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    
    # API configuration
    aena_base_url: str = "https://www.aena.es/sites/Satellite"
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """Create settings from environment variables"""
        return cls(
            default_airport_code=os.getenv('DEFAULT_AIRPORT_CODE', 'PMI'),
            plots_output_dir=os.getenv('PLOTS_OUTPUT_DIR', 'output/plots'),
            reports_output_dir=os.getenv('REPORTS_OUTPUT_DIR', 'output/reports'),
            raw_data_dir=os.getenv('RAW_DATA_DIR', 'data/raw'),
            processed_data_dir=os.getenv('PROCESSED_DATA_DIR', 'data/processed'),
            
            # Email settings
            email_smtp_server=os.getenv('EMAIL_SMTP_SERVER'),
            email_smtp_port=int(os.getenv('EMAIL_SMTP_PORT', '587')),
            email_username=os.getenv('EMAIL_USERNAME'),
            email_password=os.getenv('EMAIL_PASSWORD'),
            email_from=os.getenv('EMAIL_FROM'),
            email_to=os.getenv('EMAIL_TO'),
            
            # Telegram settings
            telegram_bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
            telegram_chat_id=os.getenv('TELEGRAM_CHAT_ID'),
            
            # API settings
            aena_base_url=os.getenv('AENA_BASE_URL', 'https://www.aena.es/sites/Satellite'),
        )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def set_settings(settings: Settings) -> None:
    """Set the global settings instance (useful for testing)"""
    global _settings
    _settings = settings