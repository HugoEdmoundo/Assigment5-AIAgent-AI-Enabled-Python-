from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import ToolExecution
from app.schemas.tool import ToolRequest, ToolResponse
from app.services.tool_service import ToolService
import json

router = APIRouter()
tool_service = ToolService()

@router.get("/")
async def list_tools():
    """Get all available tools"""
    return {
        "tools": tool_service.get_available_tools()
    }

@router.post("/execute", response_model=ToolResponse)
async def execute_tool(request: ToolRequest, db: Session = Depends(get_db)):
    """Execute a specific tool and log it to database"""
    try:
        result = tool_service.execute_tool(request.tool_name, request.parameters)
        
        # Log execution to database
        execution = ToolExecution(
            tool_name=request.tool_name,
            parameters=json.dumps(request.parameters),
            result=json.dumps(result),
            success=1
        )
        db.add(execution)
        db.commit()
        
        return ToolResponse(
            tool_name=request.tool_name,
            result=result,
            success=True
        )
    except ValueError as e:
        # Log failed execution
        execution = ToolExecution(
            tool_name=request.tool_name,
            parameters=json.dumps(request.parameters),
            result=str(e),
            success=0
        )
        db.add(execution)
        db.commit()
        
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        execution = ToolExecution(
            tool_name=request.tool_name,
            parameters=json.dumps(request.parameters),
            result=str(e),
            success=0
        )
        db.add(execution)
        db.commit()
        
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_tool_history(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent tool execution history"""
    executions = db.query(ToolExecution).order_by(
        ToolExecution.executed_at.desc()
    ).limit(limit).all()
    
    return {
        "history": [
            {
                "id": ex.id,
                "tool_name": ex.tool_name,
                "executed_at": ex.executed_at.isoformat(),
                "success": bool(ex.success)
            }
            for ex in executions
        ]
    }
