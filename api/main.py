from fastapi import FastAPI
from api.routers import restaurant_router, user_router
app = FastAPI();

@app.get("/")
def root():
    return {"Hello":"World"}  

app.include_router(restaurant_router)
app.include_router(user_router)