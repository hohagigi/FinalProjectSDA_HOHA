import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from my_classes import MyDataFrame
import mlflow
import joblib

from catboost import CatBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from keras.layers import Dense
from keras import Sequential
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score
from sklearn.utils.class_weight import compute_class_weight
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
    
mydf = MyDataFrame(start_train_date='2021-08-01',
                   end_train_date='2025-09-01',
                   start_test_date='2025-09-01',
                   end_test_date='2025-12-31',
                   )

def TrainCatBoosts(mydf):
    print (mydf.GetXTrain())
    # 2. Configurăm MLflow
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("CatBoosts")

    # 3. Antrenăm și logăm cu MLflow
    with mlflow.start_run(run_name="CatBoosts"):
        mlflow.set_tag("mlflow.note.content", "Xtrain doar 3 ani")
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
        joblib.dump(model, "models/all_CB.pkl")
        #model.save_model("models/all_CB.cbm")
        feature_importances = model.get_feature_importance()
        sns.barplot(x=feature_importances, y=mydf.GetXTrain().columns)
        plt.show()
        prediction = model.predict(mydf.GetXTest())
        #rounded_prediction = np.argmax(prediction,axis=-1)
        rounded_prediction = prediction
        y_true = np.array(mydf.GetYTest()).ravel()
        y_pred = np.array(rounded_prediction).ravel()

        cm = confusion_matrix(y_true, y_pred)

        print (cm)
        cm_plots_label = ['gazde','egalitate','oaspeti']    
        cl_repo = classification_report(y_true=mydf.GetYTest(), y_pred=rounded_prediction, target_names=cm_plots_label,output_dict=True)
        print (cl_repo)    

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
       
##  NN




def TrainNN(mydf):
    plt.figure(figsize=(10,6))
    sns.heatmap(mydf.GetXTrain().corr(), annot=True, cmap='coolwarm')
    plt.show()
    ##mydf.GetXTest().to_csv("forChatGPT.csv")
    # print (mydf.GetXTrain()[:10:])
    # print (mydf.GetXTest())
    # print (mydf.GetYTrain())
    # print (mydf.GetYTest())

    mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")

    # Create a new MLflow Experiment
    #mlflow.create_experiment("NN All Divisions")
    mlflow.set_experiment("NN All Divisions")
    mlflow.autolog()


    batch_size= 16
    epochs = 50
    learning_rate=0.001

    ## setez afisarea cu doa zecimale (nu notatia stiintifica cu 2 zecimale)
    pd.set_option('display.float_format', lambda x: f"{x:.2f}")

    with mlflow.start_run():
        mlflow.set_tag("mlflow.note.content", "Xtrain doar 3 ani")
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True )

        scaler = StandardScaler()  # incerc si RobustScaler ; StandarsScaler nu da rezultate bune
        #scaler = RobustScaler() # cu robust scaler nu obtin rezultate remarcabile. Chiar mai proaste decat cu Standard Scaler
        #print (mydf.GetXTrain()[100:130:])
        stats = pd.DataFrame({
            'min': mydf.GetXTrain().min(),
            'max': mydf.GetXTrain().max(),
            'std': mydf.GetXTrain().std(),
            'mean': mydf.GetXTrain().mean()
        })
        
        print(stats)
        X_train = pd.DataFrame(scaler.fit_transform(mydf.GetXTrain()))
        stats = pd.DataFrame({
            'min': X_train.min(),
            'max': X_train.max(),
            'std': X_train.std(),
            'mean': X_train.mean()
        })
        
        print(stats)
        #X_train = mydf.GetXTrain()
        y_train = mydf.GetYTrain()
        ##X_train.format("{:.2f}")
        ## era de la numpy , dar acum Xtrain este dataframe np.set_printoptions(precision=2, suppress=True)
        print (X_train[:10:])
        stats = pd.DataFrame({
            'min': X_train.min(),
            'max': X_train.max(),
            'std': X_train.std(),
            'mean': X_train.mean()
        })
        
        print(stats)
        print(np.unique(y_train, return_counts=True))
        pd.set_option('display.float_format', lambda x: f"{x:.2f}")
        print (type(X_train))
        print (X_train[:10:])
        
        print (mydf.GetXTrain()[:10:])
        print (mydf.GetXTest()[:10:])
        
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
        
        # feature_importances = model.get_feature_importance()
        # sns.barplot(x=feature_importances, y=mydf.GetXTrain().columns)
        # plt.show()
        
        print (history.history.keys())
        print ("Train loss:", history.history['loss'])
        print ("Val loss:", history.history['val_loss'])
        print ("Train acc:", history.history['accuracy'])
        print ("Val acc:", history.history['val_accuracy'])
        
        mlflow.log_params({"epochs":epochs})
        mlflow.log_param("batch_size", batch_size)

        model.save("models/all.keras")
        X_pred_scaled = scaler.transform(mydf.GetXTest())
        #X_pred_scaled = mydf.GetXTest()
        ## nu se foloseste fit_transform pentru X-ul pred ci doar transform    
        prediction = model.predict(x=X_pred_scaled, batch_size=20, verbose = 2)
        print (prediction[:10])
        rounded_prediction = np.argmax(prediction,axis=-1)
        y_true = np.array(mydf.GetYTest()).ravel()
        y_pred = np.array(rounded_prediction).ravel()

        cm = confusion_matrix(y_true, y_pred, labels=[0,1,2])

        print (cm)
        cm_plots_label = ['gazde','egalitate','oaspeti']    
        cl_repo = classification_report(y_true=mydf.GetYTest(), y_pred=rounded_prediction, target_names=cm_plots_label,output_dict=True)
        print (cl_repo)    

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
                


def TrainDT(mydf):
    # 2. Configurăm MLflow
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("DecisionTree_3classes")

    # 3. Antrenăm și logăm cu MLflow
    with mlflow.start_run(run_name="DT_clasificare_3_clase"):
        mlflow.set_tag("mlflow.note.content", "Xtrain doar 3 ani")
        # Model
        clf = DecisionTreeClassifier(
            criterion="gini", 
            max_depth=12,
            random_state=42
        )
        
        clf.fit(mydf.GetXTrain(), mydf.GetYTrain())
        joblib.dump(clf, "models/all_DT.pkl")
        print ("aaaa")
        print (mydf.GetXTest())
        print(np.isinf(mydf.GetXTest()).sum().sum())  # câte valori inf sunt în X_train
        prediction = clf.predict(mydf.GetXTest())
        print (prediction)
        #rounded_prediction = np.argmax(prediction,axis=-1)
        y_true = np.array(mydf.GetYTest()).ravel()
        y_pred = np.array(prediction).ravel()

        cm = confusion_matrix(y_true, y_pred)

        print (cm)
        cm_plots_label = ['gazde','egalitate','oaspeti']    
        cl_repo = classification_report(y_true=mydf.GetYTest(), y_pred=prediction, target_names=cm_plots_label,output_dict=True)
        print (cl_repo)    

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
        
        mlflow.set_tag("mlflow.note.content", "Train Decision Tree")



TrainCatBoosts(mydf=mydf)
TrainNN(mydf=mydf)
TrainDT(mydf=mydf)



"""

dupa ce fac fit_transform am in X_train ceva de genul 
     min   max  std  mean
0  -0.16 43.44 1.00  0.00
1  -2.30 28.28 1.00  0.00
2  -0.34 38.02 1.00 -0.00
3  -6.47  7.55 1.00 -0.00
4  -7.59  6.96 1.00 -0.00
5  -9.23  7.91 1.00 -0.00
6  -8.15  8.14 1.00 -0.00
7  -1.73  3.59 1.00 -0.00
8  -1.61  3.91 1.00 -0.00
9  -1.85  3.63 1.00  0.00
10 -1.53  3.88 1.00  0.00
11 -3.08  3.05 1.00  0.00
12 -2.24  3.07 1.00  0.00
13 -2.28  3.06 1.00 -0.00


cum introduc in features GM1,GM2,GP1,GP2 se duce totul in clasa 1
GM1, GM2, GP1, GP2
au valori mici (0.4 → 2.4), deci modelul:

nu vede nicio corelație puternică

gradientul este mic

modelul învață „predict clasa majoritară și gata"
"""


 
    
