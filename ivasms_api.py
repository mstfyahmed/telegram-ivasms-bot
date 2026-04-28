import requests
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List
from config import Config
from retrying import retry

logger = logging.getLogger(__name__)

class IvaSmsAPI:
    """IvaSms Panel API Integration"""
    
    def __init__(self):
        self.api_url = Config.IVASMS_API_URL
        self.panel_url = Config.IVASMS_PANEL_URL
        self.cookies_path = Config.IVASMS_COOKIE_PATH
        self.session = requests.Session()
        self.cookies = {}
        self.load_cookies()
    
    def load_cookies(self) -> bool:
        """Load IvaSms cookies from file"""
        try:
            with open(self.cookies_path, 'r') as f:
                self.cookies = json.load(f)
            logger.info("✅ IvaSms cookies loaded successfully")
            return True
        except FileNotFoundError:
            logger.error(f"❌ Cookies file not found: {self.cookies_path}")
            logger.warning("Please create cookies.json with your IvaSms session")
            return False
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON in {self.cookies_path}")
            return False
    
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Make API request with retry logic"""
        try:
            url = f"{self.api_url}{endpoint}"
            headers = kwargs.pop('headers', {})
            headers['User-Agent'] = 'TelegramIvaSmsBot/1.0'
            
            kwargs['timeout'] = Config.REQUEST_TIMEOUT
            kwargs['cookies'] = self.cookies
            kwargs['headers'] = headers
            
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None
    
    def get_sms(self, date: str, to_date: Optional[str] = None, limit: int = 50) -> Optional[Dict]:
        """
        Get SMS messages from a specific date
        
        Args:
            date: Start date (DD/MM/YYYY)
            to_date: End date (DD/MM/YYYY) - optional
            limit: Maximum messages to return
        
        Returns:
            Dict with SMS data or None
        """
        try:
            params = {
                'date': date,
                'limit': limit
            }
            if to_date:
                params['to_date'] = to_date
            
            result = self._make_request('GET', '/sms', params=params)
            if result and result.get('status') == 'success':
                logger.info(f"✅ Retrieved {len(result.get('otp_messages', []))} SMS messages")
                return result
            else:
                logger.warning(f"API returned error: {result}")
                return None
        except Exception as e:
            logger.error(f"Error fetching SMS: {e}")
            return None
    
    def get_latest_sms(self, limit: int = 50) -> Optional[List[Dict]]:
        """Get latest SMS messages"""
        today = datetime.now().strftime('%d/%m/%Y')
        result = self.get_sms(date=today, limit=limit)
        
        if result and 'otp_messages' in result:
            return result['otp_messages']
        return None
    
    def get_sms_stats(self, date: str, to_date: Optional[str] = None) -> Optional[Dict]:
        """
        Get SMS statistics for a date range
        
        Returns:
            Dict with stats (count_sms, paid_sms, unpaid_sms, revenue)
        """
        result = self.get_sms(date=date, to_date=to_date, limit=1)
        
        if result and 'sms_stats' in result:
            return result['sms_stats']
        return None
    
    def check_api_status(self) -> bool:
        """Check if IvaSms API is accessible"""
        try:
            result = self._make_request('GET', '/')
            if result:
                logger.info("✅ IvaSms API is accessible")
                return True
            else:
                logger.error("❌ IvaSms API is not responding")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to connect to IvaSms API: {e}")
            return False
    
    def extract_otp(self, message: str) -> Optional[str]:
        """
        Extract OTP code from SMS message
        
        Looks for common OTP patterns
        """
        import re
        
        patterns = [
            r'\b\d{4,6}\b',  # 4-6 digit codes
            r'code[:\s]+(\d{4,6})',
            r'code\s*:\s*(\d+)',
            r'otp[:\s]+(\d{4,6})',
            r'password[:\s]+(\d{4,6})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1) if match.groups() else match.group(0)
        
        return None

# Initialize API
api = IvaSmsAPI()

if not api.check_api_status():
    logger.warning("⚠️  Warning: IvaSms API might not be accessible")
    logger.warning("Make sure IVASMS_API_URL is correct in .env file")
