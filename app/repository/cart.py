from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cart_item import CartItem


async def add_item(db: AsyncSession, user_id: int, product_id: int, title: str, unit_price: float) -> CartItem:
    item = CartItem(user_id=user_id, product_id=product_id, title=title, unit_price=unit_price)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

async def get_items_by_user(db: AsyncSession, user_id: int) -> list[CartItem]:
    result = await db.execute(
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .order_by(CartItem.added_at.desc(), CartItem.id.desc())
    )
    return list(result.scalars().all())

async def get_item(db: AsyncSession, user_id: int, item_id: int) -> CartItem | None:
    result = await db.execute(
        select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def delete_item(db: AsyncSession, item: CartItem) -> None:
    await db.delete(item)
    await db.commit()