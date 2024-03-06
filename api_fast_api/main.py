from fastapi import FastAPI
from routes.UserRoutes import user_router
from routes.CatRoutes import cat_router
from routes.AuthRoutes import auth_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://localhost:4200",
    "http://localhost:8080",
]



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(cat_router)
app.include_router(auth_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}