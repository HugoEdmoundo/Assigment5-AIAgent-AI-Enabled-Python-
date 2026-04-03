from typing import List, Dict
from sqlalchemy.orm import Session
from app.db.models import ChatSession, ChatMessage
import uuid
from datetime import datetime

class SessionService:
    def create_session(self, db: Session) -> str:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        session = ChatSession(session_id=session_id)
        db.add(session)
        db.commit()
        return session_id
    
    def get_session(self, db: Session, session_id: str) -> ChatSession:
        """Get session by ID"""
        return db.query(ChatSession).filter(
            ChatSession.session_id == session_id
        ).first()
    
    def add_message(
        self, 
        db: Session, 
        session_id: str, 
        role: str, 
        content: str
    ) -> ChatMessage:
        """Add message to session"""
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content
        )
        db.add(message)
        
        # Update session timestamp
        session = self.get_session(db, session_id)
        if session:
            session.updated_at = datetime.utcnow()
        
        db.commit()
        return message
    
    def get_messages(
        self, 
        db: Session, 
        session_id: str, 
        limit: int = 50
    ) -> List[ChatMessage]:
        """Get messages from session"""
        return db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.asc()).limit(limit).all()
    
    def get_conversation_history(
        self, 
        db: Session, 
        session_id: str, 
        limit: int = 10
    ) -> List[Dict[str, str]]:
        """Get conversation history formatted for LLM"""
        messages = self.get_messages(db, session_id, limit)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
