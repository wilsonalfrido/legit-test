## Dataset

## ML Deployment
Inside legit-test/api we could see the deployment script for this application. The deployment use XGBoost model.

API:
- /test : to check whether api is running or not
- /api/v1/forecast/qty: generate forecasting of qty_total per week for each group menu.

### 1. Create Docker container

```bash
docker build -t app-name .

docker run -p 80:80 app-name
```
