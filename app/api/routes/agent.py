from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.agent import AgentRequest, AgentResponse, ChatRequest, ChatResponse, StreamChatRequest
from app.services.agent_service import AgentService
from app.services.session_service import SessionService
import json

router = APIRouter()
agent_service = AgentService()
session_service = SessionService()

@router.post("/query", response_model=AgentResponse)
async def process_query(request: AgentRequest, db: Session = Depends(get_db)):
    """Process agent query and execute appropriate tools"""
    response = await agent_service.process_query(
        request.query, 
        request.session_id,
        db,
        request.tools
    )
    return response

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Chat with AI agent"""
    # Create session if not provided
    session_id = request.session_id
    if not session_id:
        session_id = session_service.create_session(db)
    
    response = await agent_service.process_query(
        request.message,
        session_id,
        db
    )
    
    return ChatResponse(
        message=request.message,
        response=response.summary,
        tools_used=response.tools_used,
        session_id=session_id
    )

@router.post("/chat/stream")
async def chat_stream(request: StreamChatRequest, db: Session = Depends(get_db)):
    """Stream chat response"""
    session_id = request.session_id
    if not session_id:
        session_id = session_service.create_session(db)
    
    # Get conversation history
    conversation_history = session_service.get_conversation_history(
        db, session_id, limit=10
    )
    
    # Add user message
    session_service.add_message(db, session_id, "user", request.message)
    
    # Prepare messages for LLM
    messages = conversation_history + [
        {"role": "user", "content": request.message}
    ]
    
    async def generate():
        full_response = ""
        async for chunk in agent_service.llm_service.chat_stream(messages):
            full_response += chunk
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        
        # Save assistant response
        session_service.add_message(db, session_id, "assistant", full_response)
        yield f"data: {json.dumps({'done': True, 'session_id': session_id})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.post("/session/create")
async def create_session(db: Session = Depends(get_db)):
    """Create new chat session"""
    session_id = session_service.create_session(db)
    return {"session_id": session_id}

@router.get("/session/{session_id}/history")
async def get_session_history(session_id: str, db: Session = Depends(get_db)):
    """Get session chat history"""
    messages = session_service.get_messages(db, session_id)
    return {
        "session_id": session_id,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }

@router.get("/status")
async def agent_status():
    """Get agent status and capabilities"""
    return {
        "status": "active",
        "available_tools": agent_service.get_available_tools(),
        "version": "0.1.0",
        "features": ["sessions", "streaming", "litellm"]
    }
