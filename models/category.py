from beanie import Document, Indexed
from pydantic import Field


class Category(Document):
    name: Indexed(str, unique=True)
    description: str | None = None

    class Settings:
        name = "categories"
