from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import json


class ConversationEntryBase(SQLModel):
    conversation_id: int = Field(nullable=False, foreign_key="conversation.id")
    role: str = Field(max_length=10, nullable=False)  # "user" or "assistant"
    content: str = Field(nullable=False)


class ConversationEntry(ConversationEntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[str] = Field(default=None)  # JSON string
    tool_responses: Optional[str] = Field(default=None)  # JSON string