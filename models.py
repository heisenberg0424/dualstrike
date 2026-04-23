from pydantic import BaseModel
from typing import List, Optional


class OrderRequest(BaseModel):
    exchanges: List[str]
    symbol: str
    side: str  # 'buy' or 'sell'
    amount: float


class OrderResult(BaseModel):
    exchange: str
    success: bool
    order_id: Optional[str] = None
    symbol: Optional[str] = None
    side: Optional[str] = None
    amount: Optional[float] = None
    price: Optional[float] = None
    error: Optional[str] = None
