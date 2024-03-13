
import sys

from fastapi import HTTPException
from sqlalchemy.orm import Session
from Api.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from Api.models.Transaction import Transaction
from sqlalchemy import extract,func
from datetime import datetime

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
    

def get_transactions(db: Session, user_id: str, user_role: int, offset: int = 0, limit: int = 10):
    if user_role == "admin":
        transactions = db.query(Transaction).offset(offset).limit(limit).all()
    else:
        transactions = db.query(Transaction).filter(Transaction.user_id == user_id).offset(offset).limit(limit).all()

    if not transactions:
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
    


def get_total_month_income(db: Session, user_id: int, user_role: str):
    total_income = None
    current_month = datetime.now().month

    if user_role == "admin":
        total_income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.t_type == "revenue",
            extract('month', Transaction.t_date) == current_month
        ).scalar()
    else:
        total_income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.t_type == "revenue",
            Transaction.user_id == user_id,
            extract('month', Transaction.t_date) == current_month
        ).scalar()

    if not total_income:
        raise HTTPException(status_code=404, detail="No se encontraron ingresos")

    return total_income
    

