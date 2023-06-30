import pandas as pd
import xgboost as xgb
import json
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split


def preprocessing_testing_data(menu_group):
    #load dataset 
    df = pd.read_csv('interview-test.csv')
    df = df[df.menu_group == menu_group].copy()


    try:
        df["salesdate"] = pd.to_datetime(df["salesdate"],format="%Y-%m-%d")
        df.set_index("salesdate",inplace = True)
    except:
        pass

    
    patternFS = r'^((\[).+(\])).*'
    df['FS'] = df['menuname'].str.contains(patternFS)
    
    patternB1G1 = r'(B1G1)'
    df['B1G1'] = df['menuname'].str.contains(patternB1G1)
    
    df.drop(columns=['menuid','menuname','menu_group'],axis = 1,inplace=True)
    df['qty_total'] = df['qty_total'].apply(lambda x: int(x))
    
    df_weekly = df.resample("W").sum()
    

    #split X and Y
    X = df_weekly
    y = df_weekly['qty_total'].copy()

    return X,y


def forecast_testing_data(menu_group,num_weeks):

    X,y = preprocessing_testing_data("Gyudon Aburi with Miso Mayo & Sambal Korek")

    trainX, testX,trainY, testY = train_test_split(X,y,test_size=0.3,shuffle=False)

    scaler = MinMaxScaler()

    trainX_scaled = scaler.fit_transform(trainX)
    testX_scaled = scaler.transform(testX)

    dTest =xgb.DMatrix(data=testX_scaled)
    model_xgb = xgb.Booster()
    model_xgb.load_model(f"savedmodel/{menu_group}.json")
    yPred = model_xgb.predict(dTest)
    mae = mean_absolute_error(testY, yPred)

    df_eval = testY.to_frame()
    df_eval['pred'] = yPred
    
    tuple_eval = list(zip(df_eval.index,df_eval["qty_total"],df_eval.pred))[:num_weeks]
    dict_eval = dict((str(date), [yAct,yPred]) for date, yAct, yPred in tuple_eval)

    return dict_eval



    