from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query

from static import products
from validation import Item

app = FastAPI()

@app.get("/items", response_model=list[Item])
def get_items(
    name: Annotated[str | None, Query(min_length=2)] = None,
    min_price: Annotated[float | None, Query(gt=0)] = None,
    max_price: Annotated[float | None, Query(gt=0)] = None,
    limit: Annotated[int | None, Query(gt=9, lt=101)] = 10
):
    
    if max_price and min_price:
        if min_price >= max_price:
            raise HTTPException(status_code=400, detail="Max price must be greater than min price")
        filtered_products = [product for product in products if product["price"] >= min_price and product["price"] <= max_price ][:limit]
    elif(min_price):
        filtered_products = [product for product in products if product["price"] >= min_price][:limit]
    elif(max_price):
        filtered_products = [product for product in products if product["price"] <= max_price][:limit]
    else:
        filtered_products = products
    
    
    if (name):
        


        filtered_products = [product for product in filtered_products if product["name"] == name][:limit]
        
        return filtered_products

    

    return filtered_products


    

@app.get("/items/{item_id}", response_model=Item)    
def get_item_by_id(
    item_id: Annotated[int, Path(gt=0)],
):
    for product in products:
        if product["id"] == item_id:
            return product
    
    raise HTTPException(status_code=404, detail="Item not found")
    

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    new_item = {
        "id": len(products) + 1,
        "name": item.name,
        "price": item.price,
        "desc": item.desc
    }
    products.append(new_item)
    return new_item

