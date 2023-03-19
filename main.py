from fastapi import FastAPI
from enum import Enum
from typing import Union
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class Modelname(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()

@app.get("/")
async def show():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"description": "this is an amazing item that has a long description"}
        )
    return item

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: Modelname):
    if model_name is Modelname.alexnet:
        return {"model_name": model_name, "message":"Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}  #By enums the items in the class can be accessed by the value attributes
    
    return {"model_name":model_name, "message":"Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]



@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Union[str,None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item

@app.get("/items/stocks/{item_id}")
async def item_stock(item_id: int, short:bool = False):
    if item_id<9:
        return "Item Number should be three digit"
    else:
        return "All items are out of stock"


@app.post("/items/")
async def create_item(item: Item):
    if item.tax:
        item_dict = item.dict()
        total_tax = item.price + item.tax
        item_dict.update({'total_tax':total_tax})
        return item_dict
    

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    result = {'item_id':item_id, **item.dict()}
    return result