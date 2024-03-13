from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.security import create_access_token, verify_token
from db.connection import get_session
from Api.schemas.users import UserCreate, UserCreateAdmin, UserRead, Token, UserUpdateAdmin, UserUpdate
from Api.crud.users import authenticate_user, create_new_user, get_user_by_email, get_user_by_id, update_user, get_users

router = APIRouter()

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    user_id = await verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_db = get_user_by_id(user_id, db)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db

@router.post("/create-user/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_session)):
   
    verify_user = get_user_by_email(user.mail, db)
    if verify_user is not None:
        raise HTTPException(status_code=404, detail="email already exists")
    
    return create_new_user(user, 'user',db)
    
@router.post("/create-admin/", response_model=UserRead)
async def create_user(user: UserCreateAdmin, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user),):
   
   if current_user.user_role == "admin":
        verify_user = get_user_by_email(user.mail, db)
        if verify_user is None:
            return create_new_user(user, user.user_role,db)
        raise HTTPException(status_code=404, detail="email already exists")
        
   raise HTTPException(status_code=401, detail="Not authorized")

@router.get("/get/{user_id}", response_model=UserRead)
def read_user(user_id:str, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin" or current_user.user_id == user_id:
       
        user = get_user_by_id(user_id, db)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    raise HTTPException(status_code=401, detail="invalid token")

#ruta para el incio de sesion
@router.post("/login/",response_model=Token)
async def login_for_acces_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalided username or password", headers={"WWW-Authenticate":"Bearer"})
    
    access_token = create_access_token(data={"sub":user.user_id})
    return {"access_token":access_token, "token_type":"bearer"}


@router.put("/update-admin/", response_model=UserRead)
async def update_users(user: UserUpdateAdmin, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    verify_user = get_user_by_email(user.mail, db)
    if verify_user is not None and verify_user.user_id != user.user_id:
        raise HTTPException(status_code=404, detail="email already exists")
    if current_user.user_role == "admin":
        return update_user(user, user.user_status,user.user_role,db)
    raise HTTPException(status_code=401, detail="Not authorized")

@router.put("/update-user/", response_model=UserRead)
async def update_users(user: UserUpdate, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_id == user.user_id:
        if user.mail is not None:
            verify_user = get_user_by_email(user.mail, db)
            if verify_user is not None and verify_user.user_id != user.user_id:
                raise HTTPException(status_code=404, detail="email already exists")
    
        return update_user(user,None,None, db)
    raise HTTPException(status_code=401, detail="Not authorized")


@router.get("/get-all-users/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        return get_users(db)
    raise HTTPException(status_code=401, detail="Not authorized")