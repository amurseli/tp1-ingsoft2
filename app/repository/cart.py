from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cart_item import CartItem



async def add_item(db: AsyncSession, user_id: int, product_id: int, title: str, unit_price: float) -> CartItem:
    """Add an item to a user's cart and return it."""
    item = CartItem(user_id=user_id, product_id=product_id, title=title, unit_price=unit_price)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

async def get_items_by_user(db: AsyncSession, user_id: int) -> list[CartItem]:
    """Return all cart items for a user, ordered by addedAt desc, id desc."""
    result = await db.execute(
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .order_by(CartItem.added_at.desc(), CartItem.id.desc())
    )
    return list(result.scalars().all())

async def get_item(db: AsyncSession, user_id: int, item_id: int) -> CartItem | None:
    """Return a cart item by ID that belongs to the given user, or None."""
    result = await db.execute(
        select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def delete_item(db: AsyncSession, item: CartItem) -> None:
    """Delete a single cart item."""
    await db.delete(item)
    await db.commit()

async def delete_all_items(db: AsyncSession, user_id: int) -> None:
    """Delete all cart items for a user."""
    await db.execute(delete(CartItem).where(CartItem.user_id == user_id))
    await db.commit()