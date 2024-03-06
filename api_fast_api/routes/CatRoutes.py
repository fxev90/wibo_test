from config.db import get_mongo_client
from fastapi import APIRouter, HTTPException, Path, status, Response, Query
from models.Cat import Cat, CatCreate

db = get_mongo_client()
cat_router = APIRouter()

@cat_router.post("/cats/", response_model=Cat, tags=["cats"])
async def create_cat(cat_create: CatCreate):
    cat_model = cat_create.dict()
    db.cats.insert_one(cat_model)
    return cat_model

@cat_router.get("/cats/", response_model=list[Cat], tags=["cats"])
async def read_cats():
    cats =  db.cats.find()
    return cats


