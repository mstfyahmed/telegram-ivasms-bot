import re
from config import Config
from typing import Optional

def format_phone_number(number: str) -> str:
    """Format phone number for display"""
    if number.startswith('+'):
        return number
    elif number.startswith('1'):
        return f"+{number}"
    else:
        return f"+{number}"

def extract_otp_code(message: str) -> Optional[str]:
    """
    Extract OTP code from message
    
    Looks for common patterns:
    - 4-6 digit codes
    - Code: XXXX
    - OTP: XXXX
    """
    patterns = [
        r'\b(\d{4,6})\b',
        r'code[:\s]+(\d{4,6})',
        r'otp[:\s]+(\d{4,6})',
        r'password[:\s]+(\d{4,6})',
        r'\[?(\d{4,6})\]?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def get_service_emoji(service: str) -> str:
    """Get emoji for service"""
    service_lower = service.lower()
    service_emojis = {
        'whatsapp': '📱',
        'telegram': '💬',
        'facebook': '👍',
        'instagram': '📷',
        'twitter': '🐦',
        'google': '🔍',
        'tiktok': '🎵',
        'discord': '💬',
    }
    return service_emojis.get(service_lower, '📱')

def get_country_emoji(country: str) -> str:
    """Get emoji for country"""
    country_lower = country.lower()
    country_emojis = {
        'us': '🇺🇸',
        'uk': '🇬🇧',
        'ca': '🇨🇦',
        'au': '🇦🇺',
        'in': '🇮🇳',
        'br': '🇧🇷',
        'mx': '🇲🇽',
        'de': '🇩🇪',
        'fr': '🇫🇷',
        'ru': '🇷🇺',
    }
    return country_emojis.get(country_lower, '🌍')

def truncate_message(message: str, length: int = 100) -> str:
    """Truncate message to length"""
    if len(message) > length:
        return message[:length-3] + '...'
    return message
