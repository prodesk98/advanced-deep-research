from datetime import datetime
from typing import Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4


class Message(BaseModel):
    id: UUID4 = Field(default_factory=lambda: uuid4())
    namespace: Optional[UUID4] = Field(default=None, description="Namespace of the Message")
    role: Literal[
        "agent",
        "user"
    ] = Field(default="agent", description="Role of the Message participant")
    content: str = Field(description="Content of the Message")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation date of the Message")
