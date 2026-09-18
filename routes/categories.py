from fastapi import APIRouter
from models.category import Category

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/")
async def create_category(category: Category):
    await category.insert()
    return category


@router.get("/")
async def get_categories():
    return await Category.find().to_list()
