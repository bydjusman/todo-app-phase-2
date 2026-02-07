"""API Router for AI Conversational Agent"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from sqlmodel import Session, select
from datetime import datetime
from ..core.agent_service import TodoAgentService
from ..database.session import get_session
from ..core.auth import get_current_user_from_token
from ..models.conversation import Conversation
from ..models.conversation_entry import ConversationEntry
from fastapi.security import OAuth2PasswordBearer


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None  # Existing conversation ID (creates new if not provided)
    token: Optional[str] = None  # Token for authentication if needed


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]]


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/{user_id}", response_model=ChatResponse)
async def chat_endpoint(user_id: int, request: ChatRequest):
    """Handle a single step in the conversation with MCP tools - follows the required API specification"""
    try:
        with get_session() as session:
            # Validate user exists
            user = get_current_user_from_token(request.token, session) if request.token else None
            if not user or user.id != user_id:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or expired token or user mismatch"
                )

            # Get or create conversation
            if request.conversation_id:
                conversation = session.get(Conversation, request.conversation_id)
                if not conversation or conversation.user_id != user_id:
                    raise HTTPException(
                        status_code=404,
                        detail="Conversation not found or doesn't belong to user"
                    )
            else:
                # Create new conversation
                conversation = Conversation(user_id=user_id, title=f"Chat {datetime.now().isoformat()}")
                session.add(conversation)
                session.commit()
                session.refresh(conversation)

            # Store user message in database
            user_message = ConversationEntry(
                conversation_id=conversation.id,
                role="user",
                content=request.message
            )
            session.add(user_message)
            session.commit()

            # Fetch conversation history from database
            stmt = (
                select(ConversationEntry)
                .where(ConversationEntry.conversation_id == conversation.id)
                .order_by(ConversationEntry.timestamp)
            )
            entries = session.exec(stmt).all()

            # Build message array for agent (history + new message)
            conversation_history = []
            for entry in entries:
                conversation_history.append({
                    "role": entry.role,
                    "content": entry.content,
                    "timestamp": entry.timestamp.isoformat()
                })

            # Process the conversation with agent
            agent_service = TodoAgentService(session)
            response_text, tool_calls = await agent_service.process_message_with_tools(
                user_id=user_id,
                message=request.message,
                conversation_id=conversation.id,
                conversation_history=conversation_history
            )

            # Store assistant response in database
            assistant_response = ConversationEntry(
                conversation_id=conversation.id,
                role="assistant",
                content=response_text,
                tool_calls=str(tool_calls) if tool_calls else None
            )
            session.add(assistant_response)
            session.commit()

            # Return response with conversation ID
            return ChatResponse(
                conversation_id=conversation.id,
                response=response_text,
                tool_calls=tool_calls
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Simple chat endpoint for frontend compatibility
@router.post("/", response_model=ChatResponse)
async def simple_chat_endpoint(request: ChatRequest, user_id: int = None):
    """Simple chat endpoint for frontend compatibility - expects user_id in request body or token"""
    try:
        with get_session() as session:
            # Try to get user from token if provided
            user = get_current_user_from_token(request.token, session) if request.token else None

            # If user_id is provided in the function parameter, use that
            # Otherwise, if user exists from token, use their ID
            effective_user_id = user_id if user_id is not None else (user.id if user else None)

            if effective_user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="User identification required"
                )

            # Get or create conversation
            if request.conversation_id:
                conversation = session.get(Conversation, request.conversation_id)
                if not conversation or conversation.user_id != effective_user_id:
                    raise HTTPException(
                        status_code=404,
                        detail="Conversation not found or doesn't belong to user"
                    )
            else:
                # Create new conversation
                conversation = Conversation(user_id=effective_user_id, title=f"Chat {datetime.now().isoformat()}")
                session.add(conversation)
                session.commit()
                session.refresh(conversation)

            # Store user message in database
            user_message = ConversationEntry(
                conversation_id=conversation.id,
                role="user",
                content=request.message
            )
            session.add(user_message)
            session.commit()

            # Fetch conversation history from database
            stmt = (
                select(ConversationEntry)
                .where(ConversationEntry.conversation_id == conversation.id)
                .order_by(ConversationEntry.timestamp)
            )
            entries = session.exec(stmt).all()

            # Build message array for agent (history + new message)
            conversation_history = []
            for entry in entries:
                conversation_history.append({
                    "role": entry.role,
                    "content": entry.content,
                    "timestamp": entry.timestamp.isoformat()
                })

            # Process the conversation with agent
            agent_service = TodoAgentService(session)
            response_text, tool_calls = await agent_service.process_message_with_tools(
                user_id=effective_user_id,
                message=request.message,
                conversation_id=conversation.id,
                conversation_history=conversation_history
            )

            # Store assistant response in database
            assistant_response = ConversationEntry(
                conversation_id=conversation.id,
                role="assistant",
                content=response_text,
                tool_calls=str(tool_calls) if tool_calls else None
            )
            session.add(assistant_response)
            session.commit()

            # Return response with conversation ID
            return ChatResponse(
                conversation_id=conversation.id,
                response=response_text,
                tool_calls=tool_calls
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))