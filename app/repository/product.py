from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product


async def create_product(db: AsyncSession, seller_id: int, title: str, description: str, price: float) -> Product:
    """Create a new product and return it."""
    product = Product(seller_id=seller_id, title=title, description=description, price=round(price, 2))
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_product(db: AsyncSession, product_id: int) -> Product | None:
    """Return a product by ID, or None if not found."""
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()


async def get_all_products(db: AsyncSession) -> list[Product]:
    """Return all products ordered by ID ascending."""
    result = await db.execute(select(Product).order_by(Product.id.asc()))
    return list(result.scalars().all())


async def update_product(db: AsyncSession, product: Product, title: str, description: str, price: float) -> Product:
    """Update a product's mutable fields and return it."""
    product.title = title
    product.description = description
    product.price = round(price, 2)
    await db.commit()
    await db.refresh(product)
    return product

async def delete_product(db: AsyncSession, product: Product) -> None:
    """Delete a product from the database."""
    await db.delete(product)
    await db.commit()