from config.db import get_mongo_client
from fastapi import APIRouter, HTTPException, Path, status, Response, Query
from models.Cat import Cat, CatCreate
from bson import ObjectId

db = get_mongo_client()
cat_router = APIRouter()

@cat_router.post("/cats/", response_model=Cat, tags=["cats"])
async def create_cat(cat_create: CatCreate):
    try:
        cat_model = cat_create.dict()
        db.cats.insert_one(cat_model)
        return cat_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating cat: {str(e)}")

@cat_router.get("/cats/", response_model=list[Cat], tags=["cats"])
async def read_cats(
    name: str = None,
    breed: str = None,
    age: int = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
):
    try:
        # Construct the filter based on query parameters
        filter_params = {}
        if name:
            filter_params["name"] = name
        if breed:
            filter_params["breed"] = breed
        if age is not None:
            filter_params["age"] = age

        # Apply the filter and pagination
        cats = db.cats.find(filter_params).skip((page - 1) * limit).limit(limit)

        # Convert the MongoDB cursor to a list of dictionaries
        cat_list = [cat for cat in cats]

        return cat_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cats: {str(e)}")


@cat_router.get("/cats/{cat_id}", response_model=Cat, tags=["cats"])
async def read_cat(cat_id: str):
    try:
        cat_model = db.cats.find_one(ObjectId(cat_id))
        if cat_model is None:
            raise HTTPException(status_code=404, detail="Cat not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error retrieving cats: {str(e)}")
    return cat_model



@cat_router.put("/cats/{cat_id}", response_model=Cat, tags=["cats"])
async def update_cat(cat_id: str, cat_update: CatCreate):
    existing_cat = db.cats.find_one_and_update({"_id": ObjectId(cat_id)}, {"$set": cat_update.dict()})
    if existing_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return existing_cat

@cat_router.delete("/cats/{cat_id}",status_code=status.HTTP_204_NO_CONTENT, tags=["cats"])
async def delete_cat(cat_id: str):
    cat_model = db.cats.find_one_and_delete({'_id':ObjectId(cat_id)})
    if cat_model is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT, content="Cat removed successfully")