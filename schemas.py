from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal

# --- Input Validation ---
class OrderInput(BaseModel):
    symbol: str = Field(..., pattern=r"^[A-Z0-9]{5,12}$") # Ensures valid crypto pair format
    side: Literal["BUY", "SELL"]
    type: Literal["MARKET", "LIMIT"]
    quantity: float = Field(..., gt=0) # Must be greater than 0
    price: Optional[float] = Field(None, ge=0) # Greater or equal to 0 if provided
    timeInForce: Optional[Literal["GTD", "GTC", "IOC"]] = Field(None)

    @field_validator('price')
    @classmethod
    def check_limit_price(cls, v, info):
        if info.data.get('order_type') == 'LIMIT' and v is None:
            raise ValueError("Price is required for LIMIT orders")
        return v

# --- Output Validation ---
class OrderResponse(BaseModel):
    orderId: int
    symbol: str
    side: str
    type: str
    status: str
    price: float
    avgPrice: float