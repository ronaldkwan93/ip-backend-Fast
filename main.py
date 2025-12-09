from random import randint
from typing import Union
from pydantic import BaseModel


from fastapi import FastAPI, HTTPException, Response

app = FastAPI()

class PropertyCreate(BaseModel):
    property_suburb: str
    property_price: int


data = [
    {
        "property_id": 1,
        "property_suburb": "Burwood",
        "property_price": 100000
    },
     {
        "property_id": 2,
        "property_suburb": "Strathfield",
        "property_price": 200000
    }
]


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/properties")
def read_all_properties():
    return data

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/properties/{prop_id}")
def read_single_property(prop_id: int):
    for property in data:
        if property.get("property_id") == prop_id:
            return property
        
    return {"Property not found!"}
        
@app.post("/properties")
def create_property(body: PropertyCreate):
    count = len(data) + 1

    new = {
        "property_id": count,
        "property_suburb": body.property_suburb,
        "property_price": body.property_price
    }

    data.append(new)

    return {"property": new}

@app.put("/properties/{id}")
def update_property(body: PropertyCreate, id : int):
    for index, property in enumerate(data):
        if property.get("property_id") == id:

            updated = {
                "property_id": id,
                "property_suburb": body.property_suburb,
                "property_price": body.property_price
            }
        
            data[index] = updated
        
            return {"property": updated}
    
    return {"property not found"}

@app.delete("/properties/{id}")
def delete_property(id:int):
    for index,property in enumerate(data):
        if property.get("property_id") == id:
            data.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404)
