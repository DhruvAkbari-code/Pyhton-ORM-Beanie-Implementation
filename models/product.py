from datetime import datetime, timezone
from typing import Annotated

import pymongo

from beanie import (
    DocumentWithSoftDelete,
    Indexed,
    Link,
    before_event,
    Insert,
    Replace,
    Save,
)

from .category import Category


class Product(DocumentWithSoftDelete):
    name: Annotated[str, Indexed()]
    description: Annotated[str, Indexed(index_type=pymongo.TEXT)]
    price: float
    stock: int = 0
    category: Link[Category]
    tags: list[str]
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "products"
        use_cache = True
        cache_capacity = 100
        use_revision = False
        use_state_management = True
        state_management_save_previous = True
        validate_on_save = True
        indexes = [
            [
                ("price", pymongo.ASCENDING),
            ],
            [
                ("stock", pymongo.ASCENDING),
            ],
        ]

    @before_event(Insert, Replace, Save)
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)
