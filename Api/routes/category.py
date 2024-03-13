from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_session
from Api.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from Api.schemas.users import UserRead
from Api.crud.Category import create_new_category, get_categories, update_category, get_category_search
from Api.routes.users import get_current_user

router = APIRouter()

@router.post("/create-category/", response_model=CategoryRead)
async def create_category(category: CategoryCreate, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        return create_new_category(category, db)
    raise HTTPException(status_code=401, detail="Not authorized")

@router.get("/get-categories/", response_model=list[CategoryRead])
def read_categories(db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user is not None:
        return get_categories(db)
    raise HTTPException(status_code=401, detail="invalid token")

@router.put("/update-category/", response_model=CategoryRead)
async def update_category_route(category: CategoryUpdate, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        update_category =update_category(category, db)
        if update_category is not None:
            return update_category
        raise HTTPException(status_code=404, detail="Category not found")
    raise HTTPException(status_code=401, detail="Not authorized")

@router.get("/search-category/{search}", response_model=list[CategoryRead])
def search_category(search:str, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user is not None:
        return get_category_search(search,db)
    raise HTTPException(status_code=401, detail="invalid token")

@router.delete("/delete-category/{category_id}", response_model=CategoryRead)
def delete_category(category_id:int, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        delete_category = delete_category(category_id, db)
        if delete_category is not None:
            return delete_category
        raise HTTPException(status_code=404, detail="Category not found")
    raise HTTPException(status_code=401, detail="Not authorized")