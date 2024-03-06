from fastapi import FastAPI
from routes.UserRoutes import userRouter
from routes.CatRoutes import cat_router
app = FastAPI()
app.include_router(userRouter)
app.include_router(cat_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}