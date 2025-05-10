from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Session, select

from app.db import engine


class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"

class ClientSuscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    status: StatusEnum = Field(default=StatusEnum.active)
    suscription_id: int = Field(foreign_key="suscription.id")

class Suscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None, max_length=80)
    price: int = Field(default=None)
    clients: list["Client"] = Relationship(
                                        back_populates="suscriptions",
                                        link_model=ClientSuscription)

class ClientBase(SQLModel):
    name: str = Field(default=None, max_length=80)
    age: int = Field(default=None)
    email: EmailStr = Field(default=None, max_length=80)

    # def validate(self):
    #     if self.age < 18:
    #         raise ValueError("Client must be at least 18 years old")
    #     if not self.email:
    #         raise ValueError("Email is required")
    #     if not isinstance(self.email, EmailStr):
    #         raise ValueError("Invalid email format")

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        session = Session(engine)
        existing_client = session.exec(select(Client).where(Client.email == value)).first()
        if existing_client:
            raise ValueError("Email already exists")
        if not value:
            raise ValueError("Email is required")
    
        return value
        


class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class Client(ClientBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="client")
    suscriptions: list["Suscription"] = Relationship(
                                        back_populates="clients",
                                        link_model=ClientSuscription)
 

class TransactionBase(SQLModel):
    amount: int = Field(default=None)
    description: str = Field(default=None, max_length=80)


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    client: Client = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
    client_id: int = Field(foreign_key="client.id")

class Invoice(BaseModel):
    id: int
    client: ClientBase
    transaction: list[Transaction]
    ammount: int
    description: str
    date: str

    @property
    def total_amount(self) -> int:
        return sum(transaction.amount for transaction in self.transaction)