## Dataset
- salesdate: the day sales happen
- menuid: menu identification for the menu. (sometimes same menuname not gruanted to have identical menuid)
- menuname: name of the menu. (FS means flash sales, B1G1 means buy 1 get 1, etc)
- qty_total: total of menu ordered

## ML Deployment
Inside legit-test/api we could see the deployment script for this application. The deployment use XGBoost model.

API:
- /test : to check whether api is running or not
- /api/v1/forecast/qty: generate forecasting of qty_total per week for each group menu. This api return demand forecasting for each weak in dictionary format: {"sales_date":[actual_qty_total,prediction_qty_total]}. Here is the Input body to API:
  - num_weeks: how many weeks need to be forecasted
  - menu_group: menu_group that want to be forecasted. Due to limited data for each menu_group and limited time for training, so only 4 menu_group that can only be forecasted, e.g: ["Chicken Katsu Don","Gyudon Aburi with Miso Mayo & Sambal Korek","Sei Sultan sambal rica","Spaghetti Bolognese Brulee"]

Here is the step to run the model using Docker:
### 1. Create Docker container

```bash
docker build -t app-image-name .

docker run -d --name container-name -p 5000:5000 app-image-name
```
or you can get the image by pulling the image from docker hub:
```bash
docker pull wilsonalfrido/tech-test
```
### 2. Forecast the demand using API
GET demand forecasting data using API above in POSTMAN by accessing port 5000:
<p align="left">
    <img src="contents/api request in postman.png" alt="Model Architecture" height="300">
</p>

Or we can run the model using Uvicorn, by type the command below in terminal and get demand forecasting data using API above in POSTMAN by accessing port 8000:
```bash
cd /api
uvicorn main:app --reload
```


