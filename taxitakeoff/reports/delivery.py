from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import os


class DeliveryProvider(ABC):
    """Abstract base class for delivery providers"""
    
    @abstractmethod
    def send_report(self, pdf_filepath: str, subject: str, message: str) -> bool:
        """Send a PDF report"""
        pass


class EmailDeliveryProvider(DeliveryProvider):
    """Email delivery provider - placeholder implementation"""
    
    def __init__(self, smtp_config: Optional[Dict[str, Any]] = None):
        self.smtp_config = smtp_config or {}
        # TODO: Initialize email client with config
    
    def send_report(self, pdf_filepath: str, subject: str, message: str) -> bool:
        """Send PDF report via email"""
        # TODO: Implement email sending
        print(f"[EMAIL] Would send PDF report: {pdf_filepath}")
        print(f"[EMAIL] Subject: {subject}")
        print(f"[EMAIL] Message: {message}")
        return True


class TelegramDeliveryProvider(DeliveryProvider):
    """Telegram delivery provider - placeholder implementation"""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token
        self.chat_id = chat_id
        # TODO: Initialize Telegram bot
    
    def send_report(self, pdf_filepath: str, subject: str, message: str) -> bool:
        """Send PDF report via Telegram"""
        # TODO: Implement Telegram sending
        print(f"[TELEGRAM] Would send PDF report: {pdf_filepath}")
        print(f"[TELEGRAM] Subject: {subject}")
        print(f"[TELEGRAM] Message: {message}")
        return True


class DeliveryService:
    """Service for managing report delivery"""
    
    def __init__(self):
        self.providers: Dict[str, DeliveryProvider] = {}
    
    def register_provider(self, name: str, provider: DeliveryProvider):
        """Register a delivery provider"""
        self.providers[name] = provider
    
    def send_report(
        self, 
        provider_name: str, 
        pdf_filepath: str, 
        subject: str = "Flight Analysis Report",
        message: str = "Please find the flight analysis report attached."
    ) -> bool:
        """Send report using specified provider"""
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        if not os.path.exists(pdf_filepath):
            raise FileNotFoundError(f"PDF file not found: {pdf_filepath}")
        
        provider = self.providers[provider_name]
        return provider.send_report(pdf_filepath, subject, message)
    
    def get_available_providers(self) -> list[str]:
        """Get list of available delivery providers"""
        return list(self.providers.keys())


def create_delivery_service() -> DeliveryService:
    """Create a delivery service with default providers"""
    service = DeliveryService()
    
    # Register default providers with placeholder configs
    service.register_provider("email", EmailDeliveryProvider())
    service.register_provider("telegram", TelegramDeliveryProvider())
    
    return service