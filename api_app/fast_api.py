import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from my_classes import MyDataFrame
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.tree import DecisionTreeClassifier

from catboost import CatBoostClassifier
from keras.layers import Dense
from keras import Sequential
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.utils.class_weight import compute_class_weight
import mysql.connector
#import mysql-connector-python
import keras
from collections import defaultdict
import math
import mlflow
import matplotlib.pyplot as plt
import seaborn as sns


mydf = MyDataFrame(start_train_date='2019-08-01',
                   end_train_date='2025-08-01',
                   start_test_date='2025-08-01',
                   end_test_date='2025-12-31',
                   )
    
def train_model_CB_and_get_confusion_matrix():

    # 2. Configurăm MLflow
    mlflow.set_tracking_uri("http://mlflow:5000")
    #mlflow.create_experiment("CatBoosts")
    mlflow.set_experiment("CatBoosts")

    # 3. Antrenăm și logăm cu MLflow
    with mlflow.start_run(run_name="CatBoosts"):
        mlflow.set_tag("mlflow.note.content", "CB train from web interface")
        # Model
        model = CatBoostClassifier(
            iterations=300, depth=11, learning_rate=0.01,
            loss_function='MultiClass', eval_metric="Accuracy",
            #class_weights=[1/0.25,1/0.25,0.9],        
            #class_weights=[1/0.26, 1/0.15, 1/0.55],
            class_weights=[1/0.44, 1/0.26, 1/0.29],# valorile reale in functioe de procentajul 1/x/2 din tot datasetul 
            verbose=10
        )
    
        # train the model
        model.fit(mydf.GetXTrain(), mydf.GetYTrain())
        #model_path = os.path.join(settings.BASE_DIR, "models", "all_CatBoosts.pkl")
        joblib.dump(model, "all_CB.pkl")
        #model.save_model("models/all_CB.cbm")
        #feature_importances = model.get_feature_importance()
        #sns.barplot(x=feature_importances, y=mydf.GetXTrain().columns)
        #plt.show()
        prediction = model.predict(mydf.GetXTest())
        #rounded_prediction = np.argmax(prediction,axis=-1)
        rounded_prediction = prediction
        y_true = np.array(mydf.GetYTest()).ravel()
        y_pred = np.array(rounded_prediction).ravel()

        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                        xticklabels=["1","x","2"],
                        yticklabels=["1","x","2"])
        plt.xlabel("Predicted label")
        plt.ylabel("True label")
        plt.title("Confusion Matrix (3 classes)")
        
        mlflow.log_figure(plt.gcf(), "confusion_matrix.png")
        plt.close()

        accuracy = accuracy_score(mydf.GetYTest(), rounded_prediction)
        mlflow.log_metric("accuracy", accuracy)
        report_dict = classification_report(
            y_true=mydf.GetYTest(), y_pred=rounded_prediction,
            target_names=["gazde", "egalitate", "oaspeti"], 
            output_dict=True
        )

        for label, metrics in report_dict.items():
            if isinstance(metrics, dict):   # skip "accuracy" which is just a float
                for metric_name, value in metrics.items():
                    mlflow.log_metric(f"{label}_{metric_name}", value)
            else:
                mlflow.log_metric(label, metrics) 
       
        cm = confusion_matrix(y_true, y_pred)
        return cm

def train_model_DT_and_get_confusion_matrix():
 # 2. Configurăm MLflow
    mlflow.set_tracking_uri("http://mlflow:5000")
    #mlflow.create_experiment("DecisionTree_3classes")

    mlflow.set_experiment("DecisionTree_3classes")

    # 3. Antrenăm și logăm cu MLflow
    with mlflow.start_run(run_name="DT_clasificare_3_clase"):
        mlflow.set_tag("mlflow.note.content", "DT from web interface")
        # Model
        clf = DecisionTreeClassifier(
            criterion="gini", 
            max_depth=12,
            random_state=42
        )
        
        clf.fit(mydf.GetXTrain(), mydf.GetYTrain())
        joblib.dump(clf, "all_DT.pkl")
        prediction = clf.predict(mydf.GetXTest())

        y_true = np.array(mydf.GetYTest()).ravel()
        y_pred = np.array(prediction).ravel()

        cm = confusion_matrix(y_true, y_pred)

        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                        xticklabels=["1","x","2"],
                        yticklabels=["1","x","2"])
        plt.xlabel("Predicted label")
        plt.ylabel("True label")
        plt.title("Confusion Matrix (3 classes)")
            
        mlflow.log_figure(plt.gcf(), "confusion_matrix.png")
        plt.close()

        accuracy = accuracy_score(mydf.GetYTest(), prediction)
        mlflow.log_metric("accuracy", accuracy)
        report_dict = classification_report(
            y_true=mydf.GetYTest(), y_pred=prediction,
            target_names=["gazde", "egalitate", "oaspeti"], 
            output_dict=True
        )

        for label, metrics in report_dict.items():
            if isinstance(metrics, dict):   # skip "accuracy" which is just a float
                for metric_name, value in metrics.items():
                    mlflow.log_metric(f"{label}_{metric_name}", value)
            else:
                mlflow.log_metric(label, metrics) 
        return cm


def train_model_NN_and_get_confusion_matrix():
    mlflow.set_tracking_uri(uri="http://mlflow:5000")

    # Create a new MLflow Experiment
    #mlflow.create_experiment("NN All Divisions")
    mlflow.set_experiment("NN All Divisions")
    
    mlflow.autolog()

    batch_size= 16
    epochs = 50
    learning_rate=0.001

    with mlflow.start_run():
        mlflow.set_tag("mlflow.note.content", "NN train from web interface")
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True )

        scaler = StandardScaler()  # incerc si RobustScaler ; StandarsScaler nu da rezultate bune
        #scaler = RobustScaler() # cu robust scaler nu obtin rezultate remarcabile. Chiar mai proaste decat cu Standard Scaler
        #print (mydf.GetXTrain()[100:130:])
        X_train = pd.DataFrame(scaler.fit_transform(mydf.GetXTrain()))
        y_train = mydf.GetYTrain()
        ##X_train.format("{:.2f}")
        ## era de la numpy , dar acum Xtrain este dataframe np.set_printoptions(precision=2, suppress=True)

        model = Sequential([
        Dense(units=64, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(units=32,activation='relu'),
        Dense(units=16,activation='relu'),
        Dense(units=3, activation='softmax')                   
        ])
        
        # model = Sequential([
        #         Dense(units=32,activation='relu'),  
        #         Dense(units=16,activation='relu'),
        #         Dense(units=3, activation='softmax')  
        # ])
        
        model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
            )
        
        ######### pun class weight  ca altfel rezultatele se duc doar in 0 si 2 (in 1 se duce 0.01%)
        class_weights = compute_class_weight(
            class_weight='balanced',
            classes=np.array([0,1,2]),
            y=y_train)
        class_weights = dict(enumerate(class_weights))
        #class_weights=[0.63, 0.20, 0.16]
        print(class_weights)    
        
        history = model.fit(x = X_train,
            y = y_train,
            batch_size = batch_size,
            epochs = epochs,
            validation_split = 0.15,
            callbacks=[early_stopping],
            shuffle = True,
            verbose = 1,
            class_weight = class_weights
            )

        mlflow.log_params({"epochs":epochs})
        mlflow.log_param("batch_size", batch_size)

        model.save("all.keras")
        X_pred_scaled = scaler.transform(mydf.GetXTest())
        #X_pred_scaled = mydf.GetXTest()
        ## nu se foloseste fit_transform pentru X-ul pred ci doar transform    
        prediction = model.predict(x=X_pred_scaled, batch_size=20, verbose = 2)
        rounded_prediction = np.argmax(prediction,axis=-1)
        y_true = np.array(mydf.GetYTest()).ravel()
        y_pred = np.array(rounded_prediction).ravel()
        cm = confusion_matrix(y_true, y_pred, labels=[0,1,2])
        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                        xticklabels=["1","x","2"],                                                                          
                        yticklabels=["1","x","2"])
        plt.xlabel("Predicted label")
        plt.ylabel("True label")
        plt.title("Confusion Matrix (3 classes)")
            
        mlflow.log_figure(plt.gcf(), "confusion_matrix.png")
        plt.close()

        accuracy = accuracy_score(mydf.GetYTest(), rounded_prediction)
        mlflow.log_metric("accuracy", accuracy)
        report_dict = classification_report(
            y_true=mydf.GetYTest(), y_pred=rounded_prediction,
            target_names=["gazde", "egalitate", "oaspeti"], 
            output_dict=True
        )

        for label, metrics in report_dict.items():
            if isinstance(metrics, dict):   # skip "accuracy" which is just a float
                for metric_name, value in metrics.items():
                    mlflow.log_metric(f"{label}_{metric_name}", value)
            else:
                mlflow.log_metric(label, metrics) 

        return cm

def predict_model_NN():

    mydb = mysql.connector.connect(user='sda', password='sda',
                                host='my_bet_db',
                                database='soccer_analysis',
                                auth_plugin='mysql_native_password')
    mycursor = mydb.cursor(dictionary=True)

    mydf = MyDataFrame(start_train_date='2013-01-01',
                    end_train_date='2025-08-01',
                    start_test_date='2025-08-01',
                    end_test_date='2025-12-31')

    new_model = keras.models.load_model('all.keras')
    scaler = StandardScaler()
    X_pred_scaled = scaler.fit_transform(mydf.GetXTestUnplayed())
    prediction = new_model.predict(X_pred_scaled, batch_size=20, verbose = 1)
    
    rounded_prediction = np.argmax(prediction,axis=-1)
    l1 = len(rounded_prediction)
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
    rounded_prediction = np.argmax(prediction,axis=-1)
    l2=len(rounded_prediction)

    for p,rp,(_,row),yt in zip(prediction,rounded_prediction,mydf.GetXTestFull().iterrows(),mydf.GetYTest()):
        #print (round(p[0],2),round(p[1],2),round(p[2],2),rp,yt ,row['id'])
        query = "update games set pred2_1={pred2_1_}, \
                    pred2_x={pred2_x_}, pred2_2={pred2_2_},pred2={pred2_} \
                    where id={id_}".format(pred2_1_=round(p[0],2), \
                    pred2_x_=round(p[1],2),pred2_2_=round(p[2],2),pred2_=rp, id_=row['id'])
        mycursor.execute (query)
       
    mydb.commit()
    mycursor.close()
    mydb.close()
    
    return l1+l2

def predict_model_CB():

    mydb = mysql.connector.connect(user='sda', password='sda',
                                host='my_bet_db',
                                database='soccer_analysis',
                                auth_plugin='mysql_native_password')
    mycursor = mydb.cursor(dictionary=True)

    mydf = MyDataFrame(start_train_date='2013-01-01',
                    end_train_date='2025-08-01',
                    start_test_date='2025-08-01',
                    end_test_date='2025-12-31'
                    )

    new_model = joblib.load("all_CB.pkl")

    prediction = new_model.predict(mydf.GetXTestUnplayed())
    l1 = len(prediction)
    for p,(_,row) in zip(prediction,mydf.GetXTestUnplayedFull().iterrows()):
    #print (round(p[0],2),row['id'])
        query = "update games set predCB={pred2_}  where id={id_}".format(pred2_=p[0],  id_=row['id'])
        #print (query)
        mycursor.execute (query)
        #print (p)
        
    prediction = new_model.predict(mydf.GetXTest())
    l2 = len(prediction)
    for p,(_,row) in zip(prediction,mydf.GetXTestFull().iterrows()):
    #print (round(p[0],2),row['id'])
        query = "update games set predCB={pred2_}  where id={id_}".format(pred2_=p[0],  id_=row['id'])
        #print (query)
        mycursor.execute (query)
        print (p)    
    mydb.commit()
    mycursor.close()
    mydb.close()
    return l1+l2


def predict_model_DT():
    mydb = mysql.connector.connect(user='sda', password='sda',
                              host='my_bet_db',
                              database='soccer_analysis',
                              auth_plugin='mysql_native_password')
    mycursor = mydb.cursor(dictionary=True)

    mydf = MyDataFrame(start_train_date='2013-01-01',
                    end_train_date='2025-08-01',
                    start_test_date='2025-08-01',
                    end_test_date='2025-12-31')

    new_model = joblib.load("all_DT.pkl")

    prediction = new_model.predict(mydf.GetXTestUnplayed())
    # print (prediction)
    l1 = len(prediction)
    for p,(_,row) in zip(prediction,mydf.GetXTestUnplayedFull().iterrows()):
    #print (round(p[0],2),row['id'])
        query = "update games set predDT={pred2_}  where id={id_}".format(pred2_=p,  id_=row['id'])
        #print (query)
        mycursor.execute (query)
        #print (p)
        
    prediction = new_model.predict(mydf.GetXTest())
    l2=len(prediction)
    for p,(_,row) in zip(prediction,mydf.GetXTestFull().iterrows()):
    #print (round(p[0],2),row['id'])
        query = "update games set predDT={pred2_}  where id={id_}".format(pred2_=p,  id_=row['id'])
        #print (query)
        mycursor.execute (query)
        #print (p)    
    mydb.commit()
    mycursor.close()
    mydb.close()
    return l1+l2

def update_clasamente():
    mydb = mysql.connector.connect(user='sda', password='sda',
                              host='my_bet_db',
                              database='soccer_analysis',
                              auth_plugin='mysql_native_password')
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("select distinct country, league_name, sezon1,sezon2 from leagues")
    #mycursor.execute("select distinct country, league_name, sezon1,sezon2 from leagues where download=1")
    sezoane = mycursor.fetchall()
    for sezon in sezoane:
        param = (sezon['country'],sezon['league_name'],sezon['sezon1'],sezon['sezon2'], \
                 sezon['country'],sezon['league_name'],sezon['sezon1'],sezon['sezon2']) 
        clasament = {}
        query1 = "(select distinct HomeTeam from games where country = %s and divizia = %s and sezon1 = %s and sezon2 = %s ) \
            union all \
               (select distinct AwayTeam from games where country = %s and divizia = %s and sezon1 = %s and sezon2 = %s ) "
        #print (query1)   
        mycursor.execute (query1,param)
        echipe = mycursor.fetchall()
        ## initializare = completez clasamentul cu echipele
        for ech in echipe:
            d1 =  {
                "gm1":0,
                "gm2":0,
                "gp1":0,
                "gp2":0,
                "coef1":[],
                "coef2":[],
                "gml3" :[],
                "gpl3": [],
                "played1":0,
                "played2":0,
                "ranking":0,
                "points":0,
                "shotsontarget_a":0,
                "shotsofftarget_a":0,
                "fouls_a":0,
                "possession_a":0,
                "dangerousattacks_a":0,
                "attacks_a":0,
                "corners_a":0,
                "offsides_a":0
                }
            clasament[ech['HomeTeam']] = d1
  
        ## parcurg cronologic meciurile din sezon si updatez datele din clasament ale echipei 
        param = (sezon['country'],sezon['league_name'],sezon['sezon1'],sezon['sezon2'])     
        query2 ="select * from games where country = %s and divizia = %s and sezon1 = %s and sezon2 = %s order by dataj asc"
        mycursor.execute (query2,param)
        rows2 = mycursor.fetchall()
        for row in rows2:
            ## sortez clasamentul dupa nr de puncte
            sorted_dict = sorted(clasament.items(), key=lambda item: (item[1]['points'],item[1]['gm1']),reverse=True) 
            ranking_home = 0
            ranking_away = 0
            etapa = 0
            for i,t in enumerate(sorted_dict):
            ## sorted_dict = [('Arsenal':{'puncte':3,'goluri_marcate':2}),(...)}]  =lista
                if (t[0] == row['HomeTeam']): 
                    ranking_home = i+1
                    etapa = t[1]['played1']+1+t[1]['played2']
                    #etapa = t[0][4]
                if (t[0] == row['AwayTeam']):
                    ranking_away = i+1
            is_normal_result = 1                    
            if (row['FTR'] ==2 and row['B365A'] > 5):
                is_normal_result = 2
            # if ((row['FTR'] == 0 or row['FTR'] == 1) and row['B365A']p<=2):
            #     is_normal_result = 2
            total_home=1
            total_away=1
            if (clasament[row['HomeTeam']]['played1'] == 0 and clasament[row['HomeTeam']]['played2']== 0) :
                total_home=1
            else:
                total_home = clasament[row['HomeTeam']]['played1'] + clasament[row['HomeTeam']]['played2'] 
                
            if (clasament[row['AwayTeam']]['played1'] ==0 and clasament[row['AwayTeam']]['played2']==0 ):
                total_away=1
            else:
                total_away = clasament[row['AwayTeam']]['played1'] + clasament[row['AwayTeam']]['played2']       
            query3 = "update games set MatchDay={md_}, \
                        HTGM1={htgm1_}, HTGM2={htgm2_}, HTGP1={htgp1_}, HTGP2={htgp2_}, \
                        ATGM1={atgm1_}, ATGM2={atgm2_}, ATGP1={atgp1_}, ATGP2={atgp2_}, \
                        HTCOEF1 ={htcoef1_},  ATCOEF1 ={atcoef1_},  \
                        HTRANKING={ranking_home_},ATRANKING={ranking_away_},\
                        HTPOINTS={htpoints_}, ATPOINTS={atpoints_}, \
                        HTPLAYED1={htplayed1_}, HTPLAYED2={htplayed2_}, \
                        ATPLAYED1={atplayed1_}, ATPLAYED2={atplayed2_}, \
                        IS_NORMAL_RESULT= {is_normal_result_} ,\
                        HT_SHOTSONTARGET_A={ht_shotsontarget_a_} ,\
                        AT_SHOTSONTARGET_A={at_shotsontarget_a_} ,\
                        HT_SHOTSOFFTARGET_A={ht_shotsofftarget_a_} ,\
                        AT_SHOTSOFFTARGET_A={at_shotsofftarget_a_} ,\
                        HT_FOULS_A={ht_fouls_a_}  ,\
                        AT_FOULS_A={at_fouls_a_}  ,\
                        HT_POSSESSION_A={ht_possession_a_} ,\
                        AT_POSSESSION_A={at_possession_a_} ,\
                        HT_DANGEROUSATTACKS_A={ht_dangerousattacks_a_}   ,\
                        AT_DANGEROUSATTACKS_A={at_dangerousattacks_a_}   ,\
                        HT_ATTACKS_A={ht_attacks_a_}    ,\
                        AT_ATTACKS_A={at_attacks_a_}    ,\
                        HT_CORNERS_A={ht_corners_a_}    ,\
                        AT_CORNERS_A={at_corners_a_}    ,\
                        HT_OFFSIDES_A={ht_offsides_a_}  ,\
                        AT_OFFSIDES_A={at_offsides_a_}  ,\
                        HTGML3={htgml3_}  ,\
                        HTGPL3={htgpl3_}  ,\
                        ATGML3={atgml3_}  ,\
                        ATGPL3={atgpl3_}   \
                        where id={id_}".format(md_=etapa,
                                               htgm1_=clasament[row['HomeTeam']]['gm1'], 
                                               htgm2_=clasament[row['HomeTeam']]['gm2'],
                                               htgp1_= clasament[row['HomeTeam']]['gp1'],
                                               htgp2_= clasament[row['HomeTeam']]['gp2'],
                                               atgm1_=clasament[row['AwayTeam']]['gm1'],
                                               atgm2_=clasament[row['AwayTeam']]['gm2'],
                                               atgp1_=clasament[row['AwayTeam']]['gp1'],
                                               atgp2_=clasament[row['AwayTeam']]['gp2'],
 
                                               htcoef1_=sum(clasament[row['HomeTeam']]['coef1'][0:6]),
                                               #htcoef2_=sum(clasament[row['HomeTeam']]['coef2'][0:5]),
                                               atcoef1_=sum(clasament[row['AwayTeam']]['coef1'][0:6]),
                                               #atcoef2_=sum(clasament[row['AwayTeam']]['coef2'][0:5]),
                                               
                                               ranking_home_=ranking_home,
                                               ranking_away_=ranking_away,
                                               htpoints_=clasament[row['HomeTeam']]['points'],
                                               atpoints_=clasament[row['AwayTeam']]['points'],
                                               htplayed1_=clasament[row['HomeTeam']]['played1'],
                                               htplayed2_=clasament[row['HomeTeam']]['played2'],
                                               atplayed1_=clasament[row['AwayTeam']]['played1'],
                                               atplayed2_=clasament[row['AwayTeam']]['played2'],
                                               is_normal_result_ = is_normal_result,
                                               
                                               ht_shotsontarget_a_ =clasament[row['HomeTeam']]['shotsontarget_a'] / total_home ,
                                               at_shotsontarget_a_ =clasament[row['AwayTeam']]['shotsontarget_a'] /total_away,
                                               ht_shotsofftarget_a_ =clasament[row['HomeTeam']]['shotsofftarget_a'] / total_home,
                                               at_shotsofftarget_a_ =clasament[row['AwayTeam']]['shotsofftarget_a'] / total_away,
                                               ht_fouls_a_  =clasament[row['HomeTeam']]['fouls_a'] / total_home,
                                               at_fouls_a_  =clasament[row['AwayTeam']]['fouls_a'] / total_away,
                                               ht_possession_a_ =clasament[row['HomeTeam']]['possession_a'] / total_home,
                                               at_possession_a_ =clasament[row['AwayTeam']]['possession_a'] /total_away,
                                               ht_dangerousattacks_a_ = clasament[row['HomeTeam']]['dangerousattacks_a'] / total_home,
                                               at_dangerousattacks_a_ = clasament[row['AwayTeam']]['dangerousattacks_a'] / total_away,
                                               ht_attacks_a_ =  clasament[row['HomeTeam']]['attacks_a'] / total_home,
                                               at_attacks_a_ =  clasament[row['AwayTeam']]['attacks_a'] / total_away,
                                               ht_corners_a_ =  clasament[row['HomeTeam']]['corners_a'] / total_home,
                                               at_corners_a_ =  clasament[row['AwayTeam']]['corners_a'] / total_away,
                                               ht_offsides_a_ = clasament[row['HomeTeam']]['offsides_a'] / total_home,
                                               at_offsides_a_ = clasament[row['AwayTeam']]['offsides_a'] / total_away,
                                               htgml3_=sum(clasament[row['HomeTeam']]['gml3'][0:3]),
                                               htgpl3_=sum(clasament[row['HomeTeam']]['gpl3'][0:3]),
                                               atgml3_=sum(clasament[row['AwayTeam']]['gml3'][0:3]),
                                               atgpl3_=sum(clasament[row['AwayTeam']]['gpl3'][0:3]),                                                 
                                               id_=row['id'])
            #print (query3)
            mycursor.execute (query3)                           
            if row['status'] == "complete":
              
                if (row['FTHG'] > row['FTAG']):
                    clasament[row['HomeTeam']]['points']+=3
                    clasament[row['AwayTeam']]['coef1'].insert(0,0)     #inserez 0 puncte
                    #dif_ranking= clasament[row['HomeTeam']]['ranking']-clasament[row['AwayTeam']]['ranking']           
                    clasament[row['HomeTeam']]['coef1'].insert(0,3)     #inserez 3 puncte           
                   
                elif (row['FTHG'] < row['FTAG']):
                    clasament[row['AwayTeam']]['points']+=3
                    clasament[row['HomeTeam']]['coef1'].insert(0,0)
                    #dif_ranking= clasament[row['AwayTeam']]['ranking']-clasament[row['HomeTeam']]['ranking']           
                    clasament[row['AwayTeam']]['coef1'].insert(0,3) 
                       
                elif (row['FTHG'] == row['FTAG']):
                    clasament[row['AwayTeam']]['points']+=1
                    clasament[row['HomeTeam']]['points']+=1
                    clasament[row['HomeTeam']]['coef1'].insert(0,1)           
                    clasament[row['AwayTeam']]['coef1'].insert(0,1)      
                    
                clasament[row['HomeTeam']]['played1']+=1
                clasament[row['AwayTeam']]['played2']+=1
                
                clasament[row['AwayTeam']]['gm2']+=row['FTAG']
                clasament[row['AwayTeam']]['gp2']+=row['FTHG']
                clasament[row['HomeTeam']]['gm1']+=row['FTHG']
                clasament[row['HomeTeam']]['gp1']+=row['FTAG']
                
                clasament[row['HomeTeam']]['gpl3'].insert(0,row['FTAG'])
                clasament[row['HomeTeam']]['gml3'].insert(0,row['FTHG'])
                clasament[row['AwayTeam']]['gml3'].insert(0,row['FTAG'])
                clasament[row['AwayTeam']]['gpl3'].insert(0,row['FTHG'])
                
                if(row['HT_SHOTSONTARGET'] and row['AT_SHOTSONTARGET']):
                    clasament[row['HomeTeam']]['shotsontarget_a'] += row['HT_SHOTSONTARGET']
                    clasament[row['AwayTeam']]['shotsontarget_a'] += row['AT_SHOTSONTARGET']
                if(row['HT_SHOTSOFFTARGET'] and row['AT_SHOTSOFFTARGET']):
                    clasament[row['HomeTeam']]['shotsofftarget_a'] +=row['HT_SHOTSOFFTARGET']
                    clasament[row['AwayTeam']]['shotsofftarget_a'] +=row['AT_SHOTSOFFTARGET']
                if(row['HT_FOULS'] and row['AT_FOULS']):
                    clasament[row['HomeTeam']]['fouls_a'] +=row['HT_FOULS']
                    clasament[row['AwayTeam']]['fouls_a'] +=row['AT_FOULS']
                if(row['HT_POSSESSION'] and row['AT_POSSESSION']):
                    clasament[row['HomeTeam']]['possession_a'] +=row['HT_POSSESSION']
                    clasament[row['AwayTeam']]['possession_a'] +=row['AT_POSSESSION']
                if (row['HT_DANGEROUSATTACKS'] and row['AT_DANGEROUSATTACKS']):                    
                    clasament[row['HomeTeam']]['dangerousattacks_a'] +=row['HT_DANGEROUSATTACKS']
                    clasament[row['AwayTeam']]['dangerousattacks_a'] +=row['AT_DANGEROUSATTACKS']
                if (row['HT_ATTACKS'] and row['AT_ATTACKS']):              
                    clasament[row['HomeTeam']]['attacks_a'] +=row['HT_ATTACKS']
                    clasament[row['AwayTeam']]['attacks_a'] +=row['AT_ATTACKS']
                if (row['HT_CORNERS'] and row['AT_CORNERS']):
                    clasament[row['HomeTeam']]['corners_a'] +=row['HT_CORNERS']
                    clasament[row['AwayTeam']]['corners_a'] +=row['AT_CORNERS']
                if (row['HT_OFFSIDES'] and row['AT_OFFSIDES']):                
                    clasament[row['HomeTeam']]['offsides_a'] +=row['HT_OFFSIDES']
                    clasament[row['AwayTeam']]['offsides_a'] +=row['AT_OFFSIDES']
                #print (row['HT_POSSESSION_A'])
            lgh =  0
            lga =  0
            htgm = 0
            htgp = 0
            atgm = 0
            atgp = 0   
                
                ## modifica parametru dupa caz cu nr de meciuri dorit pt calculul coeficientului
                ## 5 meciuri =>val_accuracy 0.6485
                
                # lgh =  sum(clasament[row['HomeTeam']]['rating'][0:4])
                # lga =  sum(clasament[row['AwayTeam']]['rating'][0:4])
                # htgm = clasament[row['HomeTeam']]['goluri_marcate']
                # htgp = clasament[row['HomeTeam']]['goluri_primite']
                # atgm = clasament[row['AwayTeam']]['goluri_marcate']
                # atgp = clasament[row['AwayTeam']]['goluri_primite']
                              
        mydb.commit()
    mycursor.execute("select count(*) as count from  games")    
    x=mycursor.fetchone()
    numar_total_inregistrari=x['count']    
    mycursor.close()
    mydb.close()
    return numar_total_inregistrari

# ---- Transformare GD (pi-transform) ----
def pi_transform(diff, b=10.0, c=3.0):
    if diff == 0:
        return 0.0
    return np.sign(diff) * c * (math.log(1.0 + abs(diff)) / math.log(b))

# ---- Algoritm Pi-ratings ----
def compute_pi_ratings(df, lambda_=0.06, gamma=0.6, b=10.0, c=3.0, init_rating=0.0):
    
    r_home = defaultdict(lambda: init_rating)
    r_away = defaultdict(lambda: init_rating)

    history = []
    for _, row in df.iterrows():
        h, a = row['HomeTeam'], row['AwayTeam']
        gh, ga = int(row['FTHG']), int(row['FTAG'])

        # ratingurile echipelor înainte de meci
        home_rating_before1 = r_home[h]
        home_rating_before2 = r_home[a]
        away_rating_before1 = r_away[h]
        away_rating_before2 = r_away[a]
        
        gd_obs = gh - ga
        y = pi_transform(gd_obs, b=b, c=c)
        y_hat = r_home[h] - r_away[a]

        error = y - y_hat

        # update ratinguri
        r_home[h] += lambda_ * error
        r_away[a] -= lambda_ * error

        # cross-learning
        r_away[h] += lambda_ * gamma * error
        r_home[a] -= lambda_ * gamma * error

        history.append({
            "match_id": row["id"],
            "HomeTeam": h,
            "AwayTeam": a,
            "home_rating_before1": home_rating_before1,
            "home_rating_before2": home_rating_before2,
            "away_rating_before1": away_rating_before1,
            "away_rating_before2": away_rating_before2,
            "gd_obs": gd_obs,
            "y": y,
            "y_hat": y_hat,
            "error": error,
            "r_home[h]": r_home[h],
            "r_away[a]": r_away[a],
            "r_away[h]": r_away[h],
            "r_home[a]": r_home[a]
        })

    return dict(r_home), dict(r_away), pd.DataFrame(history)

def update_pi_rating():
    # ---- Conectare la MySQL și citire meciuri ----
    mydb = mysql.connector.connect(user='sda', password='sda',
                                host='my_bet_db',
                                database='soccer_analysis',
                                auth_plugin='mysql_native_password')
    mycursor = mydb.cursor(dictionary=True)
    nr_rows=0
    mycursor.execute("select distinct country, league_name  from leagues")
    #mycursor.execute("select distinct country, league_name, sezon1,sezon2 from leagues where download=1")
    sezoane = mycursor.fetchall()
    for sezon in sezoane:
        
        sql = f"SELECT id, dataj, HomeTeam, AwayTeam, FTHG, FTAG FROM games where country='{sezon['country']}' and divizia='{sezon['league_name']}' ORDER BY dataj ASC"
        df = pd.read_sql(sql, mydb)

        # ---- Calculează Pi-ratings ----
        r_home, r_away, hist = compute_pi_ratings(df, lambda_=0.06, gamma=0.6)
        nr_rows+=len(hist)
        ## hist e o lista de dictionare
        # ---- Scrie ratingurile în DB  ----
        for i, row in hist.iterrows():
            query = "UPDATE games  SET hpirating1 = %s, hpirating2 = %s, apirating1 = %s , apirating2 = %s  WHERE id = %s "
            mycursor.execute(query, (row["home_rating_before1"], row["home_rating_before2"], row["away_rating_before1"], row["away_rating_before2"], row["match_id"]))
            
        mydb.commit()
    mycursor.close()
    mydb.close()
    return nr_rows

app = FastAPI()

# Ca să poți apela API-ul dintr-o pagină HTML (alt origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sau pune domeniul tău aici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/train/CB")
def run_training():
    """
    Rulează antrenarea modelului și întoarce matricea de confuzie ca JSON.
    """
    cm = train_model_CB_and_get_confusion_matrix()  # cm = numpy array (3x3)
    # transformăm în listă de liste ca să fie JSON-serializabil
    return {
        "confusion_matrix": cm.tolist()
    }
    
@app.get("/train/DT")
def run_training():
    """
    Rulează antrenarea modelului și întoarce matricea de confuzie ca JSON.
    """
    cm = train_model_DT_and_get_confusion_matrix()  # cm = numpy array (3x3)
    # transformăm în listă de liste ca să fie JSON-serializabil
    return {
        "confusion_matrix": cm.tolist()
    }
   
@app.get("/train/NN")
def run_training():
    """
    Rulează antrenarea modelului și întoarce matricea de confuzie ca JSON.
    """
    cm = train_model_NN_and_get_confusion_matrix()  # cm = numpy array (3x3)
    # transformăm în listă de liste ca să fie JSON-serializabil
    return {
        "confusion_matrix": cm.tolist()
    }    
    

@app.get("/predict/CB")
def run_training():
    """
    Rulează predictia modelului și întoarce numarul de meciuri
    """
    nrp = predict_model_CB()  
    # transformăm în listă de liste ca să fie JSON-serializabil
    return {
        "numar_predictii": nrp
    }
  
@app.get("/predict/DT")
def run_training():
    """
    Rulează predictia modelului și întoarce numarul de meciuri
    """
    nrp = predict_model_DT()  
    # transformăm în listă de liste ca să fie JSON-serializabil
    return {
        "numar_predictii": nrp
    }

@app.get("/predict/NN")
def run_training():
    """
    Rulează predictia modelului și întoarce numarul de meciuri
    """
    nrp = predict_model_NN() 
    # transformăm în listă de liste ca să fie JSON-serializabil
    return {
        "numar_predictii": nrp
    }

@app.get("/update/UpdateClasamente")
def run_training():
    """
    Rulează update clasamente si intoarce nr de inregistrari actualizate
    """
    nrp = update_clasamente() 
    # transformăm în listă de liste ca să fie JSON-serializabil
    return {
        "numar_inreg": nrp
    }
    
@app.get("/update/UpdatePiRating")
def run_training():
    """
    Rulează update pi rating si intoarce nr de inregistrari actualizate
    """
    nrp = update_pi_rating() 
    # transformăm în listă de liste ca să fie JSON-serializabil
    return {
        "numar_inreg": nrp
    }
