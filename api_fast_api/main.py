from fastapi import FastAPI
from routes.UserRoutes import user_router
from routes.CatRoutes import cat_router
app = FastAPI()
app.include_router(user_router)
app.include_router(cat_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}