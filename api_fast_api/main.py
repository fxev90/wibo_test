from fastapi import FastAPI
from routes.UserRoutes import userRouter

app = FastAPI()
app.include_router(userRouter)
@app.get("/")
async def root():
    return {"message": "Hello World"}