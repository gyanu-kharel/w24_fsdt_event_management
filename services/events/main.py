from fastapi import FastAPI, HTTPException, Depends, Header
from schemas import EventCreatedResponse, CreateEvent, GetEvents, CreateInvitation, InvitationListReponse, RespondInvite, EventsListResponse
from models import Event, Invitation
from database import events_db_collection, invitations_db_collection
import jwt
from typing import List
from fastapi.responses import Response
from bson import ObjectId
from datetime import datetime

app = FastAPI()

SECRET_KEY = "my_super_duper_secret_key"

# Dependency to check for Bearer token in the request header
async def verify_token(authorization: str = Header(...)):
    # Check if the authorization header starts with 'Bearer'
    if not authorization or not authorization.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Extract the token
    token = authorization.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/events",
          response_model=EventCreatedResponse, 
          response_model_by_alias=False)
async def create_event(request: CreateEvent, current_user=Depends(verify_token)):

    if not request.title:
        raise HTTPException(status_code=400, detail='Invalid title')
    if not request.description:
        raise HTTPException(status_code=400, detail='Invalid description')
    if not request.date:
        raise HTTPException(status_code=400, detail='Invalid date')
    if not request.start_time:
        raise HTTPException(status_code=400, detail='Invalid start time')
    if not request.end_time:
        raise HTTPException(status_code=400, detail='Invalid end time')
    
    if request.capacity < 1:
        raise HTTPException(status_code=400, detail='Invalid capacity')
    
    event = Event(
        title=request.title, 
        description=request.description, 
        location=request.location,
        capacity=request.capacity,
        date=request.date,
        start_time=request.start_time,
        end_time=request.end_time,
        creator_id=current_user['id'])
    
    event_created = await events_db_collection.insert_one(event.model_dump(by_alias=True, exclude=["id"]))

    return EventCreatedResponse(id=str(event_created.inserted_id))


@app.get("/events", response_model=List[GetEvents], response_model_by_alias=False)
async def get_events(current_user=Depends(verify_token)):
    user_id = current_user["id"]
    events = []
    events_result = events_db_collection.find({'creator_id': user_id})
    events_list = await events_result.to_list(length=None)
    for ev in events_list:
        events.append(GetEvents(
            id=str(ev["_id"]),
            title=ev["title"],
            date=ev["date"],
            description=ev["description"],
            start_time=ev["start_time"],
            end_time=ev["end_time"],
            location=ev["location"],
            capacity=ev["capacity"]
        ))

    
    return events

@app.delete("/events/{event_id}")
async def delete_event(event_id, current_user=Depends(verify_token)):
    print(event_id)
    event_obj = ObjectId(event_id)
    deleted = await events_db_collection.delete_one({'_id': event_obj})
    print(deleted)
    print(deleted.deleted_count)
    if deleted.deleted_count > 0:
        return Response(status_code=200)
    else:
        return Response(status_code=400)
    


@app.post("/events/{event_id}/invitations")
async def create_invitation(event_id, request:CreateInvitation, current_user=Depends(verify_token)):
    event = await events_db_collection.find_one({'_id': event_id})
    invitation = Invitation(event_id=event_id,
                            organizer=current_user["name"],
                            guest_id=request.user_id,
                            invited_date=str(datetime.now()))
    
    invitation_created = await invitations_db_collection.insert_one(invitation.model_dump(by_alias=True, exclude=["id"]))

    if invitation_created.inserted_id:
        return Response(status_code=200)
    else:
        return Response(status_code=400)
    


@app.get("/events/invitations", response_model=List[InvitationListReponse], response_model_by_alias=False)
async def get_invitations(current_user=Depends(verify_token)):
    invitations = invitations_db_collection.find({'guest_id': current_user["id"]})
    invitations_list = await invitations.to_list(length=None)
    result = []

    for item in invitations_list:
        event_obj = ObjectId(item["event_id"])
        event = await events_db_collection.find_one({'_id': event_obj})
        result.append(InvitationListReponse(
            id=str(item["_id"]),
            event_id=item["event_id"],
            guest_id=item["guest_id"],
            invited_date=item["invited_date"],
            is_accepted=item["is_accepted"],
            organizer=item["organizer"],
            event_date=event["date"],
            event_end_time=event["end_time"],
            event_start_time=event["start_time"],
            event_location=event["location"],
            event_title=event["title"],
            event_capacity=event["capacity"]))

    return result                   


@app.put("/events/invitations/{invite_id}")
async def respond_invite(invite_id, request:RespondInvite, current_user=Depends(verify_token)):
    invite_obj = ObjectId(invite_id)
    invitation = await invitations_db_collection.find_one({'_id': invite_obj})

    update = {"$set": {
        "is_accepted": request.confirm
    }}

    updated = await invitations_db_collection.update_one({'_id': invite_obj}, update)

    if updated.modified_count == 1:
        return Response(status_code=200)    
    else:
        return Response(status_code=400)


@app.get("/events/all", response_model=List[EventsListResponse], response_model_by_alias=False)
async def get_events(current_user=Depends(verify_token)):
    result = []
    events = events_db_collection.find()
    events_list = await events.to_list(length=None)

    for event in events_list:
        result.append(EventsListResponse(
            id = str(event["_id"]),
            title= event["title"],
            description= event["description"],
            date=event["date"],
            location=event["location"],
            start_time=event["start_time"],
            end_time=event["end_time"],
            capacity=event["capacity"]
        ))

    
    return result
