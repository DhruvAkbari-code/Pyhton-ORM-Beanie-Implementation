from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db

from routes.products import router as product_router
from routes.categories import router as category_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Benaie Product API", version="1.0.0", lifespan=lifespan)


app.include_router(product_router)
app.include_router(category_router)


@app.get("/")
async def root():
    return {"message": "Beanie Product API"}
