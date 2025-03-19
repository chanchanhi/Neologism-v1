from pydantic import BaseModel

class SlangRequest(BaseModel):
    word: str

class SlangResponse(BaseModel):
    word: str
    translation: str

class SlangUpdate(BaseModel):
    word: str
    translation: str

class SlangCreate(BaseModel):
    word: str
    translation: str