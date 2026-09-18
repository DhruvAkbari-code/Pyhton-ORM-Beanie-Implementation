from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: str
    tags: list[str] = []


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: str | None = None
    tags: list[str] | None = None
