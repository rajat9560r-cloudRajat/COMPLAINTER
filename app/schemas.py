from pydantic import BaseModel
from typing import Optional

#class to validate user's input
class Validation(BaseModel):
    name:str
    title:str
    content:str

class Postupdate(BaseModel):
    name:Optional[str] = None
    title:Optional[str]= None
    content:Optional[str]=None

class Return(BaseModel):
    id : int
    status : str
    title : str

    class Config:
        orm_mode=True