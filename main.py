from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from exchange_manager import ExchangeManager
from models import OrderRequest

manager = ExchangeManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await manager.load_all_markets()
    yield
    await manager.close()


app = FastAPI(title="Multi-Exchange Trading Tool", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get("/api/exchanges")
async def get_exchanges():
    return {"exchanges": manager.get_available_exchanges()}


@app.post("/api/orders")
async def place_orders(request: OrderRequest):
    if not request.exchanges:
        raise HTTPException(status_code=400, detail="No exchanges selected")
    if request.side not in ("buy", "sell"):
        raise HTTPException(status_code=400, detail="side must be 'buy' or 'sell'")
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="amount must be positive")

    results = await manager.place_orders(
        request.exchanges, request.symbol, request.side, request.amount
    )
    return {"results": results}
