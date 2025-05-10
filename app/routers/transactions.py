from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from app.models import Transaction, Invoice, TransactionCreate, Client
from app.db import SessionDep

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    session: SessionDep,
    ):
    transaction_data_dict =  transaction_data.model_dump()
    client = session.get(Client, transaction_data_dict["client_id"])
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Client not found")
    transaction = Transaction.model_validate(transaction_data_dict)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.get("/")
def get_list_transactions(
    session: SessionDep
):
    transactions = session.exec(select(Transaction)).all()
    return transactions

@router.post("/invoice/")
async def create_invoice(
    invoice_data: Invoice,
    # session: SessionDep
    ):
    return invoice_data