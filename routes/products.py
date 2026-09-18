from fastapi import APIRouter, HTTPException, Query
from beanie.operators import AddToSet, Inc, Set, Text

from models.product import Product
from models.category import Category
from schemas.product import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


# create Product
@router.post("/")
async def create_product(data: ProductCreate):
    category = await Category.get(data.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        category=category,
        tags=data.tags,
    )

    await product.insert()
    return product


# Read all products
@router.get("/")
async def get_products():
    products = await Product.find(fetch_links=True).to_list()

    return products


# Get one product
@router.get("/{product_id}")
async def get_product(product_id: str):
    product = await Product.get(product_id, fetch_links=True)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Search using text
@router.get("/search/text")
async def search_products(q: str):
    products = await Product.find(Text(q), fetch_links=True).to_list()
    return products


# Filter by Price
@router.get("/filter/price")
async def filter_by_price(min_price: float = 0, max_price: float = 99999):
    products = await Product.find(
        Product.price >= min_price, Product.price <= max_price, fetch_links=True
    ).to_list()
    return products


# Filter by stock
@router.get("/filter/stock")
async def filter_by_stock():
    products = await Product.find(Product.stock > 0).to_list()
    return products


# Pagination
@router.get("/page/list")
async def list_products(
    page: int = Query(default=1, ge=1), size: int = Query(default=10, ge=1, le=100)
):
    skip = (page - 1) * size
    products = await Product.find(fetch_links=True).skip(skip).limit(size).to_list()

    total = await Product.find().count()

    return {"page": page, "size": size, "total": total, "products": products}


# sorting
@router.get("/sort/price")
async def sort_by_price():
    products = await Product.find().sort(Product.price).to_list()

    return products


# Update Product
@router.patch("/{product_id}")
async def update_product(product_id: str, data: ProductUpdate):
    product = await Product.get(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.name is not None:
        product.name = data.name

    if data.description is not None:
        product.description = data.description

    if data.price is not None:
        product.price = data.price

    if data.stock is not None:
        product.stock = data.stock

    if data.tags is not None:
        product.tags = data.tags

    if data.category_id is not None:
        category = await Category.get(data.category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

        product.category = category

    await product.save()
    return product


# Partial update using $set
@router.patch("/{product_id}/price")
async def update_price(product_id: str, price: float):
    product = await Product.get(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await product.set({Product.price: price})

    return product


# Increment Stock
@router.patch("/{product_id}/stock")
async def increase_stock(product_id: str, amount: int):
    product = await Product.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await product.inc({Product.stock: amount})

    return product


# Add tag using $addtoset
@router.post("/{product_id}/tags")
async def add_tag(product_id: str, tag: str):
    product = await Product.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await product.update(AddToSet({Product.tags: tag}))
    return product


# Soft Delete
@router.delete("/{product_id}")
async def delete_product(product_id: str):
    product = await Product.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await product.delete()

    return {"message": "Product deleted"}


# Soft delete restore
@router.post("/{product_id}/restore")
async def restore_product(product_id: str):
    product = await Product.find_many_in_all(Product.id == product_id).first_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product.deleted_at = None
    await product.save()

    return product


# Hard Delete
@router.delete("/{product_id}")
async def delete_product(product_id: str):
    product = await Product.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await product.hard_delete()

    return {"message": "Product deleted"}
