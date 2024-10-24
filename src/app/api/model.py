from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator

class ApiOut(BaseModel):
    coin_name: Optional[str]
    symbol: Optional[str]
    coin_price: Optional[float] 
    coin_price_dolar: Optional[float] 
    date_consult: Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    class Config:
        from_attributes = True

class ApiFilter(BaseModel):
  symbol : str
  
  @field_validator('symbol', mode="after")
  def set_symbol_lower(cls, value):
      return value.lower() if value else value

