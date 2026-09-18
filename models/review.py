from datetime import datetime, timezone
from beanie import Document, Link

from .product import Product


class Review(Document):
    product: Link[Product]
    username: str
    rating: int
    comment: str
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "reviews"
