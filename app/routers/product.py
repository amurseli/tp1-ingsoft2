from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repository import product as product_repo
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", status_code=201)
async def create_product(body: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = await product_repo.create_product(db, body.sellerId, body.title, body.description, body.price)
    return {"data": ProductResponse.model_validate(product)}


@router.get("")
async def list_products(db: AsyncSession = Depends(get_db)):
    products = await product_repo.get_all_products(db)
    return {"data": [ProductResponse.model_validate(p) for p in products]}


@router.get("/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_repo.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"data": ProductResponse.model_validate(product)}


@router.put("/{product_id}")
async def update_product(product_id: int, body: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await product_repo.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = await product_repo.update_product(db, product, body.title, body.description, body.price)
    return {"data": ProductResponse.model_validate(product)}

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_repo.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await product_repo.delete_product(db, product)
    return Response(status_code=204)