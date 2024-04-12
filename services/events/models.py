from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from typing import Optional



PyObjectId = Annotated[str, BeforeValidator(str)]


class Event(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    title: str = Field(...)
    description: str = Field(...)
    location: str = Field(...)
    date: str = Field(...)
    start_time: str = Field(...)
    end_time: str = Field(...)
    capacity: int | None = Field(...)
    creator_id: str = Field(...)
