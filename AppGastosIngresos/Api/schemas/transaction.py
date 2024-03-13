from datetime import date
from pydantic import BaseModel

class TransactionBase(BaseModel):
    amount: float
    t_description: str
    t_type: str
    t_date: date

class TransactionCreate(TransactionBase):
    user_id: str
    category_id: int

class TransactionUpdate(TransactionBase):
    transactions_id: int

class TransactionRead(TransactionBase):
    transactions_id: int
    user_id: str
    category_id: int
    
