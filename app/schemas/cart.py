from datetime import datetime
from pydantic import BaseModel, Field


class AddCartRequest(BaseModel):
    productId: int


class CartItemResponse(BaseModel):
    id: int
    productId: int = Field(validation_alias="product_id")
    title: str
    unitPrice: float = Field(validation_alias="unit_price")
    addedAt: datetime = Field(validation_alias="added_at")

    model_config = {"from_attributes": True}

class CartResponse(BaseModel):
    userId: int
    items: list[CartItemResponse]
    totalPrice: float