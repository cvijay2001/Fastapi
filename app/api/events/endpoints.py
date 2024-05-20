from fastapi import APIRouter, Depends, status, HTTPException,Request
from api.auth.oauth2 import get_current_user
from typing import List,Annotated
from sqlalchemy.orm import Session
from database import get_db
from . import schemas as event_schemas
from ..users import schemas as user_schemas, models 
from loguru import logger
import traceback

router = APIRouter(

    prefix="/event",
    tags=['Event']
)

@router.get("/")
def read_root(request: Request, current_user: Annotated[user_schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return {"Hello": "World"}


# @router.get("/get_users",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUserWithId])
# def get_users(request: Request, current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):


@router.post("/create_event/", response_model=event_schemas.Event)
def create_event(request:Request, event: event_schemas.EventCreate, current_user: Annotated[user_schemas.User, Depends(get_current_user)],db: Session = Depends(get_db)):
    logger.info(f"request_method : {request.method} - API endpoint {'/create_event/'} called with the following data -> event_title: {event.title} and more...")
    if current_user.role not in ['admin', 'event_organizer']:
        logger.warning(f"Unauthorized attempt to create event by user with role: {current_user.role}")
        raise HTTPException(status_code=403, detail="Only admin or organizer can create events")
    try:
            # new_event = models.Event(**event.model_dump(), organizer_id=current_user.id)
        new_event = models.Event(title=event.title,description=event.description,date=event.date,location=event.location,organizer_id=current_user.id,)
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        logger.info(f"Event created by user: {current_user.username}, event ID: {new_event.id}")
        return new_event
    except Exception as e:
        logger.error(f"Error occurred while creating event:{str(e)}  - {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to create event")
    


@router.get("/get_my_events/", response_model=list[event_schemas.Event])
def get_my_events(request: Request,current_user: user_schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info(f"request_method : {request.method} - API endpoint {'/get_my_events/'} called by user: username -> {current_user.username}")
    try:
        # Fetch events based on the user's role
        if current_user.role in ['event_organizer','admin']:
            events = db.query(models.Event).filter(models.Event.organizer_id == current_user.id).all()
        # elif current_user.role == 'regular':
        else:
            logger.warning(f"user:  id:{current_user.id} trying to access my_events - exception raised")
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail={'msg':"You have not created any event yet to create you should sent request to admin to change role to event_Organizer"})
        return events
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while fetching events: {str(e)}  - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch events : Internal server error ")


@router.get("/get_events/", response_model=List[event_schemas.Event])
def get_events(request: Request, current_user: Annotated[user_schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    logger.info(f"Request method: {request.method} - API endpoint '/get_events/' called by user: {current_user.username}")
    try:
        # Fetch all events
        all_events = db.query(models.Event).all()
        return all_events
    except HTTPException as e:
        raise e    
    except Exception as e:
        logger.error(f"Error occurred while fetching events: {str(e)} - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch events: Internal server error")


