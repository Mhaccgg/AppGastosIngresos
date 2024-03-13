import sys

from Api.models.Users import User
from fastapi import HTTPException
from Api.schemas.users import UserCreate, UserRead, UserUpdate
from sqlalchemy.orm import Session
from core.security import get_hashed_password, verify_password
from core.utils import generate_user_id

def create_new_user(user: UserCreate,rol:str,db:Session):
    db_user = User(
        user_id=generate_user_id(),
        full_name=user.full_name,
        mail=user.mail,
        passhash=get_hashed_password(user.passhash),
        user_role=rol,
        user_status=user.user_status
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error al crear el usuario: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al crear el usuario: {str(e)}")


def get_user_by_email(email:str,db:Session):
    user = db.query(User).filter(User.mail==email,User.user_status==1).first()
    return user

def get_user_by_id(user_id:str,db:Session):
    user = db.query(User).filter(User.user_id==user_id).first()
    return user

def authenticate_user(email:str, password:str,db:Session):
    user = get_user_by_email(email, db)
    if not user:
        return False
    if not verify_password(password, user.passhash):
        return False
    return user
    
def update_user(user:UserUpdate,status:str,role:str,db:Session):
    db_user = get_user_by_id(user.user_id, db)
    if db_user is None:
        return None
    try:
        if user.full_name is not None :
            db_user.full_name = user.full_name
        if user.mail is not None and db_user.mail != user.mail:
            db_user.mail = user.mail
        if not verify_password(user.passhash, db_user.passhash):
            db_user.passhash = get_hashed_password(user.passhash)
        if status is not None:
            db_user.user_status = status
        if user.user_role is not None:
           db_user.user_role = role  


        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar el usuario: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al actualizar el usuario: {str(e)}")
    

def get_users(db:Session):
    users = db.query(User).filter(User.user_role == "User").all()

    
    return users
