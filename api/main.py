from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated
from pydantic import BaseModel
import csv
import codecs
from model import *

app = FastAPI()
    

@app.get("/api/v1/forecast/qty")
async def forecast(menu_group:Annotated[str, Form()],split_date: Annotated[str, Form()],num_weeks: Annotated[int, Form()]):

    menu_group_list = ["Chicken Katsu Don","Gyudon Aburi with Miso Mayo & Sambal Korek","Sei Sultan sambal rica","Spaghetti Bolognese Brulee"]
    #read csv file


    predY = forecast_testing_data(menu_group = menu_group,split_date = split_date)
    
    

    return predY

@app.get("/test")
async def test(file: UploadFile):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    list_dict_csv = []
    for rows in csvReader:             
         list_dict_csv.append(rows)
    file.file.close()

    return list_dict_csv
