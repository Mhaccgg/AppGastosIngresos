from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_session
from Api.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from Api.schemas.users import UserRead
from Api.crud.transaction import create_new_transaction, get_transactions, update_transaction
from Api.routes.users import get_current_user

router = APIRouter()

@router.post("/create-transaction/", response_model=TransactionRead)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user is not None:
        return create_new_transaction(transaction, db, current_user.user_id)
    raise HTTPException(status_code=401, detail="invalid token")

@router.get("/get-transactions/", response_model=list[TransactionRead])
def read_transactions(db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user is not None:
        return get_transactions(db, current_user.user_id, current_user.user_role)
    
    raise HTTPException(status_code=401, detail="invalid token")

@router.put("/update-transaction/", response_model=TransactionRead)
async def update_transaction_route(transaction: TransactionUpdate, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user is not None:
        update_transactio = update_transaction(transaction, db)
        if update_transactio is not None:
            return update_transactio
        raise HTTPException(status_code=404, detail="Transaction not found")
    raise HTTPException(status_code=401, detail="invalid token")


