from pydantic import BaseModel
from models import Event

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


class CreateInvitation(BaseModel):
    user_id: str


class InvitationListReponse(BaseModel):
    id: str
    event_id: str
    organizer: str
    guest_id: str
    invited_date: str
    is_accepted: bool | None
    event_title: str
    event_location: str
    event_date: str
    event_start_time: str
    event_end_time: str
    event_capacity: int | None


class RespondInvite(BaseModel):
    confirm: bool



class EventsListResponse(BaseModel):
    id: str 
    title: str
    description: str
    location: str
    date: str
    start_time: str
    end_time: str
    capacity: int | None
