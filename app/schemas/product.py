from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class ProductCreate(BaseModel):
    sellerId: int
    title: str
    description: str
    price: float = Field(ge=0.01)


class ProductUpdate(BaseModel):
    title: str
    description: str
    price: float = Field(ge=0.01)


class ProductResponse(BaseModel):
    id: int
    sellerId: int = Field(validation_alias="seller_id")
    title: str
    description: str
    price: float
    createdAt: datetime = Field(validation_alias="created_at")
    updatedAt: datetime = Field(validation_alias="updated_at")

    model_config = {"from_attributes": True}