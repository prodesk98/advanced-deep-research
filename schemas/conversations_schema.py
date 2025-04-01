from datetime import datetime
from typing import Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4


class Conversation(BaseModel):
    id: UUID4 = Field(default_factory=lambda: uuid4())
    namespace: Optional[str] = Field(None, description="Namespace of the conversation")
    role: Literal[
        "agent",
        "user"
    ] = Field(default="agent", description="Role of the conversation participant")
    content: str = Field(description="Content of the conversation")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation date of the conversation")
