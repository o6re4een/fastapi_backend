from typing import List
from fastapi import APIRouter, Depends, HTTPException
from auth import require_level
from database import get_db
from models import Ticket, User, Session as SM
from sqlalchemy.orm import Session

import pyd

ticket_router = APIRouter(
    prefix="/ticket",
    tags=["tickets"],
    responses={404: {"description": "Not found"}},
)


from sqlalchemy import select


@ticket_router.get("", response_model=List[pyd.TicketResponse])
async def read_tickets(
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
    usr=Depends(require_level(2)),
):
    offset = (page - 1) * limit
    query = select(Ticket).offset(offset).limit(limit)
    return db.execute(query).scalars().all()


@ticket_router.get("/user/{user_id}", response_model=List[pyd.TicketResponse])
async def read_user_tickets(
    user_id: int,
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
    usr=Depends(require_level(1)),
):
    offset = (page - 1) * limit
    if usr.role.name != "admin" and usr.role.name != "cashier" and usr.id != user_id:
        raise HTTPException(
            status_code=403, detail="Forbidden, You can`t get tickets of another user"
        )
    query = select(Ticket).where(Ticket.user_id == usr.id).offset(offset).limit(limit)
    return db.execute(query).scalars().all()


@ticket_router.post("", response_model=pyd.TicketResponse)
async def create_ticket(
    ticket: pyd.CreateTicket,
    db: Session = Depends(get_db),
    usr: User = Depends(require_level(1)),
):

    valdiate_ticket(ticket, db)
    if (
        usr.id != ticket.user_id
        and usr.role.name != "admin"
        and usr.role.name != "cashier"
    ):
        raise HTTPException(
            status_code=403, detail="Forbidden, You can`t buy ticket for another user"
        )

    db_ticket = Ticket(
        user_id=ticket.user_id,
        place_num=ticket.place_num,
        session_id=ticket.session_id,
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@ticket_router.put("/{id}", response_model=pyd.TicketResponse)
async def update_ticket(
    id: int,
    ticket: pyd.CreateTicket,
    db: Session = Depends(get_db),
    usr=Depends(require_level(2)),
):
    valdiate_ticket(ticket, db)
    db_ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db_ticket.user_id = ticket.user_id
    db_ticket.session_id = ticket.session_id
    db_ticket.place_num = ticket.place_num

    db.commit()
    db.refresh(db_ticket)

    return db_ticket


@ticket_router.get("/{id}", response_model=pyd.TicketResponse)
async def read_ticket(
    id: int, db: Session = Depends(get_db), usr=Depends(require_level(1))
):
    db_ticket = db.query(Ticket).filter(Ticket.id == id).first()

    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if (
        usr.id != db_ticket.user_id
        and usr.role.name != "admin"
        and usr.role.name != "cashier"
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    return db_ticket


@ticket_router.delete("/{id}", status_code=204)
async def delete_ticket(
    id: int, db: Session = Depends(get_db), usr=Depends(require_level(2))
):
    db_ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(db_ticket)
    db.commit()
    return


def valdiate_ticket(ticket: pyd.CreateTicket, db: Session) -> None:

    ticket_db = (
        db.query(Ticket)
        .filter(Ticket.user_id == ticket.user_id)
        .filter(Ticket.session_id == ticket.session_id)
        .first()
    )
    if ticket_db is not None:
        raise HTTPException(
            status_code=400, detail="User and Session is alredy in the ticket"
        )

    exist_user = db.query(User).filter(User.id == ticket.user_id).first()
    if exist_user is None:
        raise HTTPException(status_code=400, detail="User not found")

    exist_sesion = db.query(SM).filter(SM.id == ticket.session_id).first()
    if exist_sesion is None:
        raise HTTPException(status_code=400, detail="Session not found")
    return
