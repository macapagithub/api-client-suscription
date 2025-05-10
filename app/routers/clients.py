from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from app.models import (Client, ClientCreate, ClientUpdate, 
                        Suscription, ClientSuscription, StatusEnum)
from app.db import SessionDep
from app.dependencies import get_client_or_404

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)


@router.post('/', response_model=Client)
async def create_client(client_data: ClientCreate, session: SessionDep):
    client = Client.model_validate(client_data.model_dump())
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@router.get('/', response_model=list[Client])
async def get_clients(session: SessionDep):
    return session.exec(select(Client)).all()

@router.get('/{client_id}', response_model=Client)
async def get_client(client_id: int, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Client not found")
    return client

@router.delete('/{client_id}')
async def delete_client(client_id: int, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Client not found")
    session.delete(client)
    session.commit()
    return {"message": "Client deleted successfully"}

@router.patch('/{client_id}', 
           response_model=Client, 
           status_code=status.HTTP_201_CREATED)
async def update_client(client_id: int, client_data: ClientUpdate, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Client not found")
    client_data_dict = client_data.model_dump(exclude_unset=True)
    client.sqlmodel_update(client_data_dict)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.post('/{client_id}/suscribe/{susceiption_id}')
async def suscribe_client(client_id: int, suscription_id: int , 
                          session: SessionDep,
                          suscription_status: StatusEnum =Query()):
    client_db = session.get(Client, client_id)
    if not client_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Client not found")
    
    suscription_db = session.get(Suscription, suscription_id)
    if not suscription_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Suscription not found")

    client_suscription = ClientSuscription(client_id=client_db.id, 
                                           suscription_id=suscription_db.id,
                                           status=suscription_status)
    session.add(client_suscription)
    session.commit()
    session.refresh(client_suscription)
    return client_suscription
    

@router.get('/{client_id}/suscriptions')
async def get_client_suscriptions(client_id: int, session: SessionDep,
                                  suscription_status: StatusEnum =Query()):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Client not found")
    # suscriptions = session.exec(select(Suscription).join(ClientSuscription)).all()
    suscriptions = session.exec(select(ClientSuscription)
                 .where(ClientSuscription.client_id == client_id)
                 .where(ClientSuscription == suscription_status)).all()
    return suscriptions