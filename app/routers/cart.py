from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repository import cart as cart_repo
from app.repository import product as product_repo
from app.schemas.cart import AddCartRequest, CartItemResponse, CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/{user_id}/items", status_code=201)
async def add_item(user_id: int, body: AddCartRequest, db: AsyncSession = Depends(get_db)):
    product = await product_repo.get_product(db, body.productId)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    item = await cart_repo.add_item(db, user_id, product.id, product.title, product.price)
    return {"data": CartItemResponse.model_validate(item)}

@router.get("/{user_id}")
async def get_cart(user_id: int, db: AsyncSession = Depends(get_db)):
    items = await cart_repo.get_items_by_user(db, user_id)
    cart_items = [CartItemResponse.model_validate(item) for item in items]
    total = sum(item.unit_price for item in items)
    return {"data": CartResponse(userId=user_id, items=cart_items, totalPrice=round(total, 2))}

@router.delete("/{user_id}/items/{item_id}")
async def delete_item(user_id: int, item_id: int, db: AsyncSession = Depends(get_db)):
    item = await cart_repo.get_item(db, user_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    await cart_repo.delete_item(db, item)
    return Response(status_code=204)

@router.delete("/{user_id}")
async def wipe_cart(user_id: int, db: AsyncSession = Depends(get_db)):
    await cart_repo.delete_all_items(db, user_id)
    return Response(status_code=204)