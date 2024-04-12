from pydantic import BaseModel


class CreateEvent(BaseModel):
    title: str
    description: str
    location: str
    date: str
    start_time: str
    end_time: str
    capacity: int | None


class EventCreatedResponse(BaseModel):
    id: str


class GetEvents(BaseModel):
    id: str
    title: str
    description: str
    location: str
    date: str
    start_time: str
    end_time: str
    capacity: int | None