from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.post("/{num}/")
def index(num:int,limit:Optional[int]=10,published:bool=True):
    return {"limit":limit,"published":published,"num":num}