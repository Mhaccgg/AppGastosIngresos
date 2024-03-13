from pydantic import BaseModel

class CategoryBase(BaseModel):
    category_name: str
    category_description: str

class CategoryRead(CategoryBase):
    category_id: int
    category_status: bool=True

class CategoryCreate(CategoryBase):
    category_status: bool=True

class CategoryUpdate(CategoryBase):
    category_id: int
    category_status: bool=True





