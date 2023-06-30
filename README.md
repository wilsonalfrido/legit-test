## Dataset

## ML Deployment
Inside legit-test/api we could see the deployment script for this application. The deployment use XGBoost model.
How to run model using docker: 

### 1. Create Docker container

```bash
docker build -t app-name .

docker run -p 80:80 app-name
```
