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

app = FastAPI(
    title="Wibo test API",
    description="api for wibo test to connect with mongodb",
    summary="Aplication for wibo test",
    version="0.0.1",
    terms_of_service="Not available",
    contact={
        "name": "Francisco Escalante",
        "url": "https://www.linkedin.com/in/francisco-escalante-5119a3108/",
        "email": "fxev90@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(user_router)
app.include_router(cat_router)
app.include_router(auth_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}