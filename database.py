from pymongo import AsyncMongoClient
from beanie import init_beanie

from models.category import Category
from models.product import Product
from models.review import Review

MONGO_URL = "MONGO_URL"
DATABASE_NAME = "product_catalog"


async def init_db():
    client = AsyncMongoClient(MONGO_URL)

    await init_beanie(
        database=client[DATABASE_NAME],
        document_models=[
            Category,
            Product,
            Review,
        ],
    )
