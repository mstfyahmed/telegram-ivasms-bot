from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import Config
import logging

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(Config.DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    current_number = Column(String(20))
    current_service = Column(String(50))
    current_country = Column(String(50))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

class UserNumber(Base):
    """Track assigned numbers"""
    __tablename__ = 'user_numbers'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    phone_number = Column(String(20), nullable=False)
    service = Column(String(50))
    country = Column(String(50))
    otp_code = Column(String(10))
    otp_message = Column(Text)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    otp_received_at = Column(DateTime)
    expired = Column(Boolean, default=False)
    expired_at = Column(DateTime)

class BotStats(Base):
    """Bot statistics"""
    __tablename__ = 'bot_stats'
    
    id = Column(Integer, primary_key=True)
    total_users = Column(Integer, default=0)
    total_numbers = Column(Integer, default=0)
    total_otps = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create all tables
try:
    Base.metadata.create_all(engine)
    logger.info("✅ Database initialized successfully")
except Exception as e:
    logger.error(f"❌ Database initialization failed: {e}")

def get_session():
    """Get database session"""
    return Session()

def add_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None) -> bool:
    """Add or update user in database"""
    try:
        session = get_session()
        user = session.query(User).filter_by(user_id=user_id).first()
        
        if user:
            user.last_activity = datetime.utcnow()
            user.active = True
        else:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_admin=user_id in Config.ADMIN_IDS
            )
            session.add(user)
        
        session.commit()
        session.close()
        return True
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        return False

def get_user(user_id: int) -> User:
    """Get user from database"""
    try:
        session = get_session()
        user = session.query(User).filter_by(user_id=user_id).first()
        session.close()
        return user
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        return None

def add_number(user_id: int, phone_number: str, service: str = None, country: str = None) -> bool:
    """Add assigned number to database"""
    try:
        session = get_session()
        
        # Update user's current number
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.current_number = phone_number
            user.current_service = service
            user.current_country = country
        
        # Add to history
        user_number = UserNumber(
            user_id=user_id,
            phone_number=phone_number,
            service=service,
            country=country
        )
        session.add(user_number)
        session.commit()
        session.close()
        return True
    except Exception as e:
        logger.error(f"Error adding number: {e}")
        return False

def add_otp(user_id: int, otp_code: str, otp_message: str) -> bool:
    """Add OTP to user's number"""
    try:
        session = get_session()
        user_number = session.query(UserNumber).filter_by(user_id=user_id).order_by(UserNumber.id.desc()).first()
        
        if user_number:
            user_number.otp_code = otp_code
            user_number.otp_message = otp_message
            user_number.otp_received_at = datetime.utcnow()
            session.commit()
            session.close()
            return True
        return False
    except Exception as e:
        logger.error(f"Error adding OTP: {e}")
        return False

def get_all_users() -> list:
    """Get all active users"""
    try:
        session = get_session()
        users = session.query(User).filter_by(active=True).all()
        session.close()
        return users
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return []

def get_stats() -> dict:
    """Get bot statistics"""
    try:
        session = get_session()
        total_users = session.query(User).filter_by(active=True).count()
        total_numbers = session.query(UserNumber).count()
        total_otps = session.query(UserNumber).filter(UserNumber.otp_code != None).count()
        session.close()
        
        return {
            'total_users': total_users,
            'total_numbers': total_numbers,
            'total_otps': total_otps
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {'total_users': 0, 'total_numbers': 0, 'total_otps': 0}
