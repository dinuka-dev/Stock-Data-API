from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
import os, json

app = FastAPI()

class DataList(BaseModel):
    data: List[int]

class Stock(BaseModel):
    stock: str
    sector: str
    last: str
    chg_percentage: str
    change: str
    volume: str
    market_cap: str
    upcoming_earnings: Optional[str] = None

class StockList(BaseModel):
    list_id: str
    title: str
    description: Optional[str] = None
    stocks: List[Stock]

def save_list(stock_list: StockList):
    try:
        save_dir = 'data'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        list_id = stock_list.list_id
        save_path = f'{save_dir}/{list_id}.json'
        with open(save_path, 'w', encoding='utf-8') as json_file:
            json.dump(stock_list.dict(), json_file, indent=4)
        return {'status': 'success'}
    except Exception as e:
        print(e)
        return {'status': 'error'}
    
def getListData(list_id: str):
    try:
        save_dir = 'data'
        save_path = f'{save_dir}/{list_id}.json'
        with open(save_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(e)
        return {'status': 'error'}
    
def updateLiveLists(data_list: DataList):
    try:
        file_name = "live.json"
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data_list, json_file, indent=4)
        return {'status': 'success'}
    except Exception as e:
        print(e)
        return {'status': 'error'}
   
def getLiveLists():
    try:
        file_name = "live.json"
        with open(file_name, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(e)
        return {'status': 'error'}
    
@app.post("/save_list/")
async def create_stock_list(stock_list: StockList):
    res = save_list(stock_list)
    return res

@app.get("/get_list/{list_id}")
def read_root(list_id: str):
    list_id = str(list_id)
    data = getListData(list_id)
    return data

@app.post("/update_live_lists/")
async def receive_list(data_list: DataList):
    res = updateLiveLists(data_list.data)
    return res

@app.get("/get_live_lists/")
def read_root():
    data = getLiveLists()
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)