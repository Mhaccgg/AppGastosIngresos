import sys

from fastapi import HTTPException
from sqlalchemy.orm import Session
from Api.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from Api.models.Transaction import Transaction

def create_new_transaction(transaction: TransactionCreate, db:Session,user_id:str):
    db_transaction = Transaction(
        amount=transaction.amount,
        t_description=transaction.t_description,
        t_type=transaction.t_type,
        t_date=transaction.t_date,
        user_id=user_id,
        category_id=transaction.category_id
    )

    try:
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        print(f"Error al crear la transaccion: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al crear la transaccion: {str(e)}")
    

def get_transactions(db:Session,user_id:str,user_role:int):
    if user_role == "admin":
        transactions = db.query(Transaction).all()
    else:
        transactions = db.query(Transaction).filter(Transaction.user_id==user_id).all()

    if transactions is None:
        raise HTTPException(status_code=404, detail="No se encontraron transacciones")
    
    return transactions

def update_transaction(transaction:TransactionUpdate,db:Session):
    db_transaction = db.query(Transaction).filter(Transaction.transactions_id==transaction.transactions_id).first()
    if db_transaction is None:
        return None
    try:
        changes_made = False
        for attr, value in transaction.dict().items():
            if value is not None and getattr(db_transaction, attr) != value:
                setattr(db_transaction, attr, value)
                changes_made = True
        if not changes_made:
            raise HTTPException(status_code=500, detail="No se han realizado cambios")
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar la transaccion: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al  actualizar la transaccion: {str(e)}")
    

