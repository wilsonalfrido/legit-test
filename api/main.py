from fastapi import FastAPI, Form, Response
from typing import Annotated
from pydantic import BaseModel
from model import *

app = FastAPI()
    

@app.get("/api/v1/forecast/qty")
async def forecast(menu_group:Annotated[str, Form()],num_weeks: Annotated[int, Form()]):

    menu_group_list = ["Chicken Katsu Don","Gyudon Aburi with Miso Mayo & Sambal Korek","Sei Sultan sambal rica","Spaghetti Bolognese Brulee"]
    if menu_group not in menu_group_list:
        return "Menu Group not found"
    if num_weeks < 0:
        return "Number of weeks must be positive integer"
    predY = forecast_testing_data(menu_group = menu_group,num_weeks=num_weeks)

    return predY

@app.get("/test")
async def test():
    return "ML API is running ..."
