from fastapi import HTTPException, status
from app.db import SessionDep
from app.models import Client

async def get_client_or_404(client_id: int, session: SessionDep) -> Client:
    """
    Common dependency to get a client by ID or raise a 404 error
    """
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    return client