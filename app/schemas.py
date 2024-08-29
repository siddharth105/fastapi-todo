from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: str
    updated_at: Optional[str] = None

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            completed=obj.completed,
            created_at=obj.created_at.isoformat(),  # Convert to ISO format
            updated_at=obj.updated_at.isoformat() if obj.updated_at else None  # Convert to ISO format, handle None
        )

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
