from config.db import get_mongo_client
from fastapi import APIRouter, HTTPException, Path, status, Response, Query, Depends
from models.Cat import Cat, CatCreate, CatResponse
from bson import ObjectId
from auth.jwt import get_current_user
from schemas.CatSchema import catSchema, catsSchema

db = get_mongo_client()
cat_router = APIRouter()

@cat_router.post("/cats/", response_model=Cat, tags=["cats"])
async def create_cat(cat_create: CatCreate, current_user: str = Depends(get_current_user)):
    """
    Create a new cat in the database.

    Parameters:
    - cat_create: a CatCreate object representing the new cat to be created.
    - current_user: a string representing the current user.

    Returns:
    - A Cat object representing the newly created cat.
    """
    try:
        cat_model = cat_create.dict()
        db.cats.insert_one(cat_model)
        return cat_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating cat: {str(e)}")

@cat_router.get("/cats/", response_model=list[CatResponse], tags=["cats"])
async def read_cats(
    name: str = None,
    breed: str = None,
    age: int = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    current_user: str = Depends(get_current_user)
):
    """
    A function to retrieve a list of cats based on optional query parameters including name, breed, and age. 
    It also handles pagination and applies filters to the MongoDB cursor.
    Returns a list of CatResponse objects.
    """
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
        cat_list = catsSchema(cats)

        return cat_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cats: {str(e)}")


@cat_router.get("/cats/{cat_id}", response_model=Cat, tags=["cats"])
async def read_cat(cat_id: str, current_user: str = Depends(get_current_user)):
    """
    Get information about a specific cat by its ID, along with the current user's authentication. 
    If the cat is not found, raise an HTTPException with a 404 status code and the detail "Cat not found". 
    If there is an error retrieving the cat, raise an HTTPException with a 404 status code and the detail containing the error message. 
    Return the cat model if found.
    """
    try:
        cat_model = db.cats.find_one(ObjectId(cat_id))
        if cat_model is None:
            raise HTTPException(status_code=404, detail="Cat not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error retrieving cats: {str(e)}")
    return cat_model



@cat_router.put("/cats/{cat_id}", response_model=Cat, tags=["cats"])
async def update_cat(cat_id: str, cat_update: CatCreate, current_user: str = Depends(get_current_user)):
    """
    Update a cat with the given cat_id using the provided cat_update.
    
    Args:
        cat_id (str): The ID of the cat to be updated.
        cat_update (CatCreate): The updated information for the cat.
        current_user (str, optional): The current user. Defaults to Depends(get_current_user).
    
    Returns:
        Cat: The updated cat information.
        
    Raises:
        HTTPException: If the cat with the given ID is not found.
    """
    existing_cat = db.cats.find_one_and_update({"_id": ObjectId(cat_id)}, {"$set": cat_update.dict()})
    if existing_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return existing_cat

@cat_router.delete("/cats/{cat_id}",status_code=status.HTTP_204_NO_CONTENT, tags=["cats"])
async def delete_cat(cat_id: str, current_user: str = Depends(get_current_user)):
    """
    Deletes a cat from the database by its ID.

    Args:
        cat_id (str): The ID of the cat to be deleted.
        current_user (str, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        Response: If successful, returns a response with status code 204 and content "Cat removed successfully".
    
    Raises:
        HTTPException: If the cat with the specified ID is not found, raises an HTTPException with status code 404 and detail "Cat not found".
    """
    cat_model = db.cats.find_one_and_delete({'_id':ObjectId(cat_id)})
    if cat_model is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT, content="Cat removed successfully")