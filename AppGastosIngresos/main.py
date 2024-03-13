from fastapi import APIRouter, FastAPI
from Api.routes import users
from Api.routes import category
from Api.routes import transaction
from core.config import settings

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(transaction.router, prefix="/transaction", tags=["transaction"])

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, description=settings.PROJECT_DESCRIPTION)  
app.include_router(api_router)

