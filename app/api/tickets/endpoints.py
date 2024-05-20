from fastapi import APIRouter, Depends, status, HTTPException,Request
from api.auth.oauth2 import get_current_user
from typing import List,Annotated
from sqlalchemy.orm import Session
from database import get_db
from . import schemas as ticket_schemas
from ..users import schemas as user_schemas, models 
from loguru import logger
import traceback

router = APIRouter(

    prefix="/event",
    tags=['Ticket']
)



@router.post("/{event_id}/tickets", response_model=ticket_schemas.Ticket)
def create_ticket(event_id: int, ticket: ticket_schemas.TicketCreate, request: Request, current_user: Annotated[user_schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    """
    This Api creates the Event Ticket , it accepts the event_id as input and based on event_id it creates the event_ticket of that Event.
    """
    logger.info(f"Request method: {request.method} - API endpoint '/events/{event_id}/tickets' called by user: {current_user.username}")

    try:
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
            logger.warning(f"Event with ID {event_id} not found.")
            raise HTTPException(status_code=404, detail="Event not found")

        if current_user.role == 'admin' or (current_user.role == 'event_organizer' and event.organizer_id == current_user.id):
            # User is authorized to create tickets
            new_ticket = models.Ticket(
                ticket_type=ticket.ticket_type,
                price=ticket.price,
                quantity=ticket.quantity,
                event_id=event_id
            )

            db.add(new_ticket)
            db.commit()
            db.refresh(new_ticket)

            logger.info(f"Ticket created for event {event.title} by user {current_user.username}: {new_ticket}")
            return new_ticket
        else:
            logger.warning(f"User {current_user.username} is not authorized to create tickets for event {event.title}")
            raise HTTPException(status_code=403, detail={"status":False,"msg":"You are not authorized to create tickets for this event"})

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while creating ticket: {str(e)} - {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"status":False,"msg":"Failed to create ticket : Internal Server Error"})


@router.patch("/{event_id}/ticket/{ticket_id}", response_model=ticket_schemas.Ticket)
def update_ticket(event_id: int, ticket_id: int, updated_ticket: ticket_schemas.TicketUpdate, request: Request, current_user: Annotated[user_schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    logger.info(f"Request method: {request.method} - API endpoint '/event/{event_id}/ticket/{ticket_id}' called by user: {current_user.username}")
    try:
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
            logger.warning(f"Event with ID {event_id} not found.")
            raise HTTPException(status_code=404, detail="Event not found")

        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id, models.Ticket.event_id == event_id).first()
        if not ticket:
            logger.warning(f"Ticket with ID {ticket_id} not found for event {event.title}.")
            raise HTTPException(status_code=404, detail="Ticket not found")

        if current_user.role == 'admin' or (current_user.role == 'event_organizer' and event.organizer_id == current_user.id):
            # User is authorized to update the ticket
            ticket.ticket_type = updated_ticket.ticket_type
            ticket.price = updated_ticket.price
            ticket.quantity = updated_ticket.quantity
            db.add(ticket)
            db.commit()
            db.refresh(ticket)

            logger.info(f"Ticket {ticket_id} updated for event {event.title} by user {current_user.username}: {ticket}")
            return ticket
        else:
            logger.warning(f"User {current_user.username} is not authorized to update ticket {ticket_id} for event {event.title}")
            raise HTTPException(status_code=403, detail="You are not authorized to update this ticket")

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while updating ticket: {str(e)} - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"status":False,"msg":"Failed to update ticket : Internal Server Error"})
    

@router.get("/{event_id}/tickets", response_model=List[ticket_schemas.Ticket])
def get_event_tickets(event_id: int, request: Request, current_user: Annotated[user_schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    logger.info(f"Request method: {request.method} - API endpoint '/event/{event_id}/tickets' called by user: username: {current_user.username}")

    try:
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
            logger.warning(f"Event with ID {event_id} not found.")
            raise HTTPException(status_code=404, detail="Event not found")

        tickets = db.query(models.Ticket).filter(models.Ticket.event_id == event_id).all()

        logger.info(f"Tickets retrieved for event_title {event.title} by user - username:{current_user.username}")
        return tickets

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while retrieving tickets: {str(e)} - {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"status":False,"msg":"Failed to retrieve tickets : Internal Server Error"})
    

@router.get("/{ticket_id}", response_model=ticket_schemas.Ticket)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            logger.warning(f"Ticket with ID {ticket_id} not found.")
            raise HTTPException(status_code=404, detail="Ticket not found")

        logger.info(f"Retrieved ticket - id:{ticket}")
        return ticket

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while retrieving ticket: {str(e)} - {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to retrieve ticket")
    


@router.delete("/{ticket_id}", summary="Delete a ticket", description="Delete a specific ticket. Only the admin or the event organizer who created the event can delete the ticket.")
def delete_ticket(request:Request,ticket_id: int, current_user: Annotated[user_schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    try:
        logger.info(f"Request method: {request.method} - API endpoint '/event/{ticket_id}' called by user: username:{current_user.username} id:{current_user.id}")
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            logger.warning(f"Ticket with ID {ticket_id} not found.")
            raise HTTPException(status_code=404, detail="Ticket not found")

        event = db.query(models.Event).filter(models.Event.id == ticket.event_id).first()

        if current_user.role == 'admin' or (current_user.role == 'event_organizer' and event.organizer_id == current_user.id):
            db.delete(ticket)
            db.commit()
            logger.success(f"Ticket with ID {ticket_id} deleted by user {current_user.username}")
            return {"message": "Ticket deleted successfully"}
        else:
            logger.warning(f"User {current_user.username} is not authorized to delete ticket {ticket_id}")
            raise HTTPException(status_code=403, detail="You are not authorized to delete this ticket")

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while deleting ticket: {str(e)} - {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"status":False,"msg":"Failed to delete ticket"})