from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from sqlalchemy import select
from database.connection import get_session
from models.events import Event, EventUpdate

event_router = APIRouter(
    tags=["Events"]
)

events = []


@event_router.get("/events", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    # statement = select(Event)
    # events = session.exec(statement).all()

    # statement = select(Event)
    # events = session.query(Event).offset(skip).limit(limit).all()
    
    events = session.query(Event).all()
    return events


@event_router.get("/events/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID: " + str(id) + " does not exist")

@event_router.post("/events")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    
    return {
        "message": "Event created successfully"
    }

@event_router.put("/events/{id}", response_model=Event)
async def update_event(id: int, new_data: EventUpdate,
session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID: " + str(id) + " does not exist")

@event_router.delete("/events/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {
                "message": "Event deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail= "Event with supplied ID: " + str(id) + " does not exist")