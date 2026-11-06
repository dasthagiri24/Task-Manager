from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: Optional[str] = None
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=150
    )
    description: Optional[str] = None
    completed: Optional[bool] = None
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    model_config = ConfigDict(from_attributes=True)