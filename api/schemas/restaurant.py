from pydantic import BaseModel
from typing import List, Optional

class RestaurantBase(BaseModel):
    name: str
    capacity: int

    
class RestaurantCreate(RestaurantBase):
    occupancy: Optional[int] = 0


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    occupancy: Optional[int] = None

class Restaurant(RestaurantBase):
    id: int
    occupancy: int
