from fastapi import FastAPI
from app.scheduler import start
from app.database import engine
from app.database import Base  
from app.api import gold_prices , exchange_rates


app = FastAPI()

@app.on_event("startup")
def startup():
    print("🔧 Creating tables if needed...")
    Base.metadata.create_all(bind=engine)
    start()

app.include_router(exchange_rates.router)
app.include_router(gold_prices.router)