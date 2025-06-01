from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    name: str
    surname: str
    studentId: str
    fump: int
  

    
class UserCreate(UserBase):
    balance: Optional[int] = 0
    fump: Optional[int] = 0

class UserUpdate(BaseModel):
    fump: Optional[int] = None
    balance: Optional[int] = None 
    name: Optional[str] = None 
    surname: Optional[str] = None 
    studentId: Optional[str] = None 

class User(UserBase):
    id: int
    balance: int
