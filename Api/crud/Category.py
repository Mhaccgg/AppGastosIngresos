import sys

from Api.models.Category import Category
from fastapi import HTTPException
from Api.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from sqlalchemy.orm import Session



def create_new_category(category: CategoryCreate, db:Session):
    db_category = Category(
        category_name=category.category_name,
        category_description=category.category_description,
    )

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        print(f"Error al crear la categoria: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al crear la categoria: {str(e)}")
    
    
def get_categories(db:Session):
    categories = db.query(Category).filter(Category.category_status==1).all()
    return categories


def update_category(category:CategoryUpdate,db:Session):
    db_category = db.query(Category).filter(Category.category_id==category.category_id).first()
    if db_category is None:
        return None
    try:
        for attr, value in category.dict().items():
            if value is not None and getattr(db_category, attr) != value:
                setattr(db_category, attr, value)
            
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar la categoria: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al actualizar la categoria: {str(e)}")
    
def get_category_search(search:str,db:Session):

    category = db.query(Category).filter(Category.category_name.like(f"%{search}%")).all()
    return category

def delete_category(category_id:int,db:Session):
    db_category = db.query(Category).filter(Category.category_id==category_id).first()
    if db_category is None:
        return None
    try:
        db_category.category_status = 0
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar la categoria: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al eliminar la categoria: {str(e)}")
