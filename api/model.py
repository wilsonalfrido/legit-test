import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error


def preprocessing_testing_data(menu_group,split_date):
    #load dataset
    df = csv_to_df(csv_dict)
    df = df[df.menu_group == menu_group].copy()

    try:
        df["salesdate"] = pd.to_datetime(df["salesdate"],format="%Y-%m-%d")
        df.set_index("salesdate",inplace = True)
    except:
        pass

    #flash shale
    patternFS = r'^((\[).+(\])).*'
    df['FS'] = df['menuname'].str.contains(patternFS)
    #buy 1 get 1
    patternB1G1 = r'(B1G1)'
    df['B1G1'] = df['menuname'].str.contains(patternB1G1)
    
    df.drop(columns=['menuid','package','menuname','salesNum','bomid','menu_group'],axis = 1,inplace=True)
    df['qty_total'] = df['qty_total'].apply(lambda x: int(x))
    
    df_weekly = df.resample("W").sum()
    

    # split X and Y
    df_test = df_weekly.loc[split_date:]
    testX = df_test
    testY = df_test['qty_total'].copy()

    return testX,testY


def forecast_testing_data(menu_group,split_date):
    testX,testY = preprocessing_testing_data(csv_dict,menu_group,split_date)

    dTest =xgb.DMatrix(data=testX)
    model_xgb = xgb.Booster()
    model_xgb.load_model(f"../saved_model/{menu_group}.json")
    yPred = model_xgb.predict(dTest)
    mae = mean_absolute_error(testY, yPred)

    eval = testY.to_frame()
    eval['pred'] = yPred
    
    tuple_eval = list(zip(eval.index,eval.pred))
    dict_eval = dict((str(date), yPred) for date, yPred in tuple_eval)

    return dict_eval


def csv_to_df(csv_dict)->pd.DataFrame:
    list_dict_csv = []
    for rows in csv_dict:             
         list_dict_csv.append(rows)
    
    df = pd.DataFrame(list_dict_csv)
    return df
    