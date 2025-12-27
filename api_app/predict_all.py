import mysql.connector

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

from keras.layers import Dense
from keras import Sequential
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score
from sklearn.utils.class_weight import compute_class_weight

from my_classes import MyDataFrame
import keras
import joblib


mydb = mysql.connector.connect(user='sda', password='sda',
                              host='my_bet_db',
                              database='soccer_analysis',
                              auth_plugin='mysql_native_password')
mycursor = mydb.cursor(dictionary=True)

mydf = MyDataFrame(
                    start_train_date='2018-01-01',
                    end_train_date='2025-12-01',
                    start_test_date='2025-10-01',
                    end_test_date='2025-12-31'
                   )

def PredictNN(mydb,mycursor,mydf):
    new_model = keras.models.load_model('models/all.keras')
    print (mydf.GetXTestFull().shape)

    print (mydf.GetXTest().shape)
    print (mydf.GetYTest().shape)
    # GetXTestUnplayed.
    scaler = StandardScaler()
    X_pred_scaled = scaler.fit_transform(mydf.GetXTestUnplayed())
    prediction = new_model.predict(X_pred_scaled, batch_size=20, verbose = 1)

    rounded_prediction = np.argmax(prediction,axis=-1)
    #print (rounded_prediction)
    y_true = np.array(mydf.GetYTestUnplayed()).ravel()
    y_pred = np.array(rounded_prediction).ravel()

    print ("y pred",y_pred)
    #print ("y true",y_true)

    cm = confusion_matrix(y_true, y_pred)

    print (cm)

    for p,rp,(_,row),yt in zip(prediction,rounded_prediction,mydf.GetXTestUnplayedFull().iterrows(),mydf.GetYTestUnplayed()):
        #print (round(p[0],2),round(p[1],2),round(p[2],2),rp,yt ,row['id'])
        query = "update games set pred2_1={pred2_1_}, \
                    pred2_x={pred2_x_}, pred2_2={pred2_2_},pred2={pred2_} \
                    where id={id_}".format(pred2_1_=round(p[0],2), \
                    pred2_x_=round(p[1],2),pred2_2_=round(p[2],2),pred2_=rp, id_=row['id'])
        mycursor.execute (query)
        #print (query)

    X_pred_scaled = scaler.fit_transform(mydf.GetXTest())
    prediction = new_model.predict(X_pred_scaled, batch_size=20, verbose = 1)

    # print (mydf.GetXTestFull().shape)
    # print (mydf.GetXTestUnplayedFull().shape)
    # print (mydf.GetYTestUnplayed().shape)
    rounded_prediction = np.argmax(prediction,axis=-1)
    #print (rounded_prediction)
    y_true = np.array(mydf.GetYTest()).ravel()
    y_pred = np.array(rounded_prediction).ravel()
    print ("y pred",y_pred)
    #print ("y true",y_true)

    for p,rp,(_,row),yt in zip(prediction,rounded_prediction,mydf.GetXTestFull().iterrows(),mydf.GetYTest()):
        #print (round(p[0],2),round(p[1],2),round(p[2],2),rp,yt ,row['id'])
        query = "update games set pred2_1={pred2_1_}, \
                    pred2_x={pred2_x_}, pred2_2={pred2_2_},pred2={pred2_} \
                    where id={id_}".format(pred2_1_=round(p[0],2), \
                    pred2_x_=round(p[1],2),pred2_2_=round(p[2],2),pred2_=rp, id_=row['id'])
        mycursor.execute (query)
        #print (query)    
   
    mydb.commit()

def PredictCB(mydb,mycursor,mydf):
    new_model = joblib.load("models/all_CB.pkl")

    prediction = new_model.predict(mydf.GetXTestUnplayed())
    for p,(_,row) in zip(prediction,mydf.GetXTestUnplayedFull().iterrows()):
    #print (round(p[0],2),row['id'])
        query = "update games set predCB={pred2_}  where id={id_}".format(pred2_=p[0],  id_=row['id'])
        #print (query)
        mycursor.execute (query)
        #print (p)
        
    prediction = new_model.predict(mydf.GetXTest())
    for p,(_,row) in zip(prediction,mydf.GetXTestFull().iterrows()):
    #print (round(p[0],2),row['id'])
        query = "update games set predCB={pred2_}  where id={id_}".format(pred2_=p[0],  id_=row['id'])
        #print (query)
        mycursor.execute (query)
        print (p)    
    mydb.commit()

    # print (mydf.GetXTest().shape)
    # print (mydf.GetXTestFull().shape)
    # print (mydf.GetYTest().shape)

    # print (mydf.GetXTestUnplayed().shape)
    # print (mydf.GetXTestUnplayedFull().shape)
    # print (mydf.GetYTestUnplayed().shape)

def PredictDT(mydb,mycursor,mydf):
    new_model = joblib.load("models/all_DT.pkl")
    print (mydf.GetXTest().shape)
    print (mydf.GetXTestFull().shape)
    print (mydf.GetYTest().shape)

    print (mydf.GetXTestUnplayed().shape)
    print (mydf.GetXTestUnplayedFull().shape)
    print (mydf.GetYTestUnplayed().shape)

    prediction = new_model.predict(mydf.GetXTestUnplayed())
    # print (prediction)

    for p,(_,row) in zip(prediction,mydf.GetXTestUnplayedFull().iterrows()):
    #print (round(p[0],2),row['id'])
        query = "update games set predDT={pred2_}  where id={id_}".format(pred2_=p,  id_=row['id'])
        #print (query)
        mycursor.execute (query)
        #print (p)
        
    prediction = new_model.predict(mydf.GetXTest())
    print (prediction)

    for p,(_,row) in zip(prediction,mydf.GetXTestFull().iterrows()):
    #print (round(p[0],2),row['id'])
        query = "update games set predDT={pred2_}  where id={id_}".format(pred2_=p,  id_=row['id'])
        #print (query)
        mycursor.execute (query)
        #print (p)    
    mydb.commit()


PredictNN(mydb=mydb,mycursor=mycursor,mydf=mydf)
PredictCB(mydb=mydb,mycursor=mycursor,mydf=mydf)
PredictDT(mydb=mydb,mycursor=mycursor,mydf=mydf)

mycursor.close()
mydb.close()
