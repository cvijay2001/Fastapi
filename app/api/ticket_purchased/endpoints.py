from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from api.auth.oauth2 import get_current_user
from typing import Annotated,List
from . import schemas as tkt_purc_schemas
from ..users import schemas as user_schemas,models
from loguru import logger
import traceback

router = APIRouter(
    prefix="/purchased_tickets",
    tags=['Purchased_Tickets']
)

@router.post("/purchase", summary="Purchase tickets", description="Purchase a specified number of tickets for an event.")
def purchase_tickets(purchase_details: tkt_purc_schemas.TicketPurchaseCreate, request: Request, current_user: Annotated[user_schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    logger.info(f"Request method: {request.method} - API endpoint '/tickets/purchase' called by user: {current_user.username}")

    try:
        ticket = db.query(models.Ticket).filter(models.Ticket.id == purchase_details.ticket_id).first()
        if not ticket:
            logger.warning(f"Ticket with ID {purchase_details.ticket_id} not found.")
            raise HTTPException(status_code=404, detail="Ticket not found")

        if ticket.quantity < purchase_details.quantity:
            logger.warning(f"Insufficient tickets available for purchase. Requested quantity: {purchase_details.quantity}, Available quantity: {ticket.quantity}")
            raise HTTPException(status_code=400, detail=f"Insufficient tickets available. Only {ticket.quantity} tickets left for this event.")

        new_purchase = models.TicketPurchased(
            quantity=purchase_details.quantity,
            ticket_id=purchase_details.ticket_id,
            user_id=current_user.id
        )

        ticket.quantity -= purchase_details.quantity
        db.add(new_purchase)
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        db.refresh(new_purchase)

        logger.info(f"Tickets purchased by user {current_user.username}: {new_purchase}")
        return new_purchase

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while purchasing tickets: {str(e)} - {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to purchase tickets")
    


@router.get("/{user_id}/purchased_tickets", summary="Get purchased tickets", description="Get a list of tickets purchased by a user.", response_model=List[tkt_purc_schemas.PurchasedTicketDetails])
def get_purchased_tickets(user_id: int, request: Request, current_user: Annotated[user_schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    logger.info(f"Request method: {request.method} - API endpoint '/users/{user_id}/purchased_tickets' called by user: {current_user.username}")

    try:
        if current_user.id != user_id and current_user.role != 'admin':
            logger.warning(f"User {current_user.username} is not authorized to access purchased tickets for user {user_id}")
            raise HTTPException(status_code=403, detail="You are not authorized to access this information")

        purchased_tickets = db.query(models.TicketPurchased, models.Ticket, models.Event) \
            .join(models.Ticket, models.TicketPurchased.ticket_id == models.Ticket.id) \
            .join(models.Event, models.Ticket.event_id == models.Event.id) \
            .filter(models.TicketPurchased.user_id == user_id) \
            .all()

        purchased_ticket_details = []
        for purchase, ticket, event in purchased_tickets:
            ticket_details = {
                "purchase_id": purchase.id,
                "quantity": purchase.quantity,
                "ticket_type": ticket.ticket_type,
                "ticket_price": ticket.price,
                "event_title": event.title,
                "event_date": event.date,
                "event_location": event.location
            }
            purchased_ticket_details.append(ticket_details)

        logger.info(f"Purchased tickets retrieved for user {user_id} by user {current_user.username}")
        return purchased_ticket_details

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error occurred while retrieving purchased tickets: {str(e)} - {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to retrieve purchased tickets")