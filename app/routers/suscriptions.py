from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.models import Suscription #, SuscriptionCreate, SuscriptionUpdate
from app.db import SessionDep

router = APIRouter(
    prefix="/suscriptions",
    tags=["suscriptions"]
)


@router.post('/', response_model=Suscription)
async def create_suscription(suscription_data: Suscription, session: SessionDep):
    suscription_db = Suscription.model_validate(suscription_data.model_dump())
    session.add(suscription_db)
    session.commit()
    session.refresh(suscription_db)
    return suscription_db

@router.get('/', response_model=list[Suscription])
async def get_suscriptions(session: SessionDep):
    return session.exec(select(Suscription)).all()