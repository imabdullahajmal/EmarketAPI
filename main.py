from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import time


# Our App
app = FastAPI()

# Our Model.
class Item(BaseModel):
    id: Optional[UUID] = None
    name: str = None
    price: float = 0.0
    desc: Optional[str] = None

# List to store our items.
items = []

def cur_time():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

# Create an item.
@app.post('/market/', response_model=Item)
def add_item(item:Item):
    item.id = uuid4()
    items.append(item)
    with open('logs.txt', 'a') as file:
        file.write('Item added. --- '+cur_time()+'\n')
        file.close()
    return item

# View an item.
@app.get('/market/{item_id}', response_model=Item)
def view_item(item_id:UUID):
    for item in items:
        if item.id==item_id:
            with open('logs.txt', 'a') as file:
                file.write('Item viewed. --- '+cur_time()+'\n')
                file.close()
            return item
    raise HTTPException(status_code=404, detail='Item not found')

# View all items.
@app.get('/market/', response_model=List[Item])
def view_items():
    with open('logs.txt', 'a') as file:
        file.write('All items viewed. --- '+cur_time()+'\n')
        file.close()
    return items

# Update an item.
@app.put('/market/{item_id}', response_model=Item)
def update_item(item_id:UUID, item_update:Item):
    for idx, item in enumerate(items):
        if item.id==item_id:
            updated_item=item.copy(update=item_update.dict(exclude_unset=True))
            items[idx]=updated_item
            with open('logs.txt', 'a') as file:
                file.write('Item updated. --- '+cur_time()+'\n')
                file.close()
            return updated_item
    raise HTTPException(status_code=404, detail='Item not found')

#Delete and item.
@app.delete('/market/{item_id}', response_model=Item)
def delete_item(item_id:UUID):
    for idx, item in enumerate(items):
        if item.id==item_id:
            items.pop(idx)
            with open('logs.txt', 'a') as file:
                file.write('Item deleted. --- '+cur_time()+'\n')
                file.close()
            return item
    
    raise HTTPException(status_code=404, detail='Item not found')

#Start the server and run the app on server 8001
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=80)

