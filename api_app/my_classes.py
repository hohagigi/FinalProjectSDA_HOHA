import mysql.connector
import numpy as np
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

class MyDataFrame:

    # constructor
    # se poate defini in mai multe moduri

    def __init__(
        self,
        start_train_date="2010-01-01",
        end_train_date=datetime.datetime.now().strftime("%Y-%m-%d"),
        start_test_date="2010-01-01",
        end_test_date=datetime.datetime.now().strftime("%Y-%m-%d"),
        country="",
        division=""
    ):
        self.__version__ = "1.0.0"
        self.start_train_date = start_train_date
        self.end_train_date = end_train_date
        self.start_test_date = start_test_date
        self.end_test_date = end_test_date
        self.country=country
        self.division=division
        mydb = mysql.connector.connect(
            user="sda",
            password="sda",
            host="my_bet_db",
            database="soccer_analysis",
            auth_plugin="mysql_native_password",
        )
        
        coloane = [
                "B365H",
                "B365D",
                "B365A",
                # "MatchDay",
                "HomeTeamCat",
                "AwayTeamCat",
                "HTGML3",        
                "HTGPL3",
                "ATGML3",
                "ATGPL3",
                # "ATGP2",
                # "GM1",            # folosite pentru diferenta dintre echipe            
                # "GM2",            
                # "GP1",            
                # "GP2",            
                "HTCOEF1",          # nr de puncte din ultimele 5 meciuri (acasa si deplasare)
                "ATCOEF1",          # nr de puncte din ultimele 5 meciuri (acasa si deplasare)
                # "HTCOEF2",        # nr de puncte din ultimele 5 meciuri  
                # "ATCOEF2",        # nr de puncte din ultimele 5 meciuri
                # "RANKING",        
                # "HTPOINTS",       
                # "ATPOINTS",
                # # "COEF1",
                # "COEF2",
                # "COEF3",
                # "COEF4",
                "hpirating1",
                "hpirating2",
                "apirating1",
                "apirating2",
                "HTRANKING",
                "ATRANKING",
                "FTR",
                # "HT_DANGEROUSATTACKS",
                # "AT_DANGEROUSATTACKS",
                # "HT_ATTACKS",
                # "AT_ATTACKS",
                # "IS_NORMAL_RESULT",
                "HT_SHOTSONTARGET_A",
                "AT_SHOTSONTARGET_A",
                "HT_SHOTSOFFTARGET_A",
                "AT_SHOTSOFFTARGET_A",
                # "HT_FOULS_A",
                # "AT_FOULS_A",
                # "HT_POSSESSION_A",
                # "AT_POSSESSION_A",
                "HT_DANGEROUSATTACKS_A",
                "AT_DANGEROUSATTACKS_A",
                "HT_ATTACKS_A",
                "AT_ATTACKS_A",
                # "HT_CORNERS_A",
                # "AT_CORNERS_A",
                # "HT_OFFSIDES_A",
                # "AT_OFFSIDES_A"
                # "predCB1",
                # "predCB2",
                # "predCB3"
                # "country_cat",
                "divizia_cat"
        ]
        
        # pentru cazul cand s-a completat tara si divizia se vor lua in calcul la query
        if (len(country)==0 and len(division)==0):
            #param = "1=1 and HTRANKING+3>=ATRANKING and HTRANKING -3<=ATRANKING "
            
            #param = "1=1 "
            param = " 1=1  and matchday>3 "
            #param = "1=1 and B365A <= 2.4 and matchday>3 "
            # param=param+" and predCB1=2 "         5 8   8 5 
            # param=param+" and  predCB2=2 " 
            
        else:
            param = f"country = '{country}' and divizia = '{division}' "
        
        # construiesc train_dataframe            
        query = f"select * from games where dataj>='{self.start_train_date}' and dataj<='{self.end_train_date}' \
            and FTR >=0  and B365H>0  and {param} order by dataj asc"
        train_dataframe = pd.read_sql(query, mydb)
        
        #construiesc  test dataframe
        query = f"select * from games where dataj>='{self.start_test_date}' and dataj<='{self.end_test_date}' \
            and B365H>0  and {param}  order by dataj asc"
        test_dataframe = pd.read_sql(query, mydb)
        self.test_dataframe_full = test_dataframe
       
        
        query = f"select * from games where FTR = -1 and {param} order by id asc"
        test_dataframe_unplayed = pd.read_sql(query, mydb)
        self.test_dataframe_unplayed_full = test_dataframe_unplayed
        
        mydb.close()

        train_dataframe["country_cat"] = (
            train_dataframe["country"].astype("category").cat.codes
        )
        train_dataframe["divizia_cat"] = (
            train_dataframe["divizia"].astype("category").cat.codes
        )
        
        train_dataframe["iswin"] = train_dataframe["FTR"].apply(lambda x: 0 if x == 0 else 1)
        # train_dataframe["dif"] = (
        #     train_dataframe["PlaceHome"] - train_dataframe["PlaceAway"]
        # )
        train_dataframe["HomeTeamCat"] = train_dataframe["HomeTeam"].astype("category").cat.codes
        train_dataframe["AwayTeamCat"] = train_dataframe["AwayTeam"].astype("category").cat.codes

        # train_dataframe['GM1'] = train_dataframe["HTGM1"]
        # train_dataframe['GM2'] = train_dataframe["HTGM2"]
        # train_dataframe['GP1'] = train_dataframe["HTGP1"]
        # train_dataframe['GP2'] = train_dataframe["HTGP2"]
        # train_dataframe['ATGM1'] = train_dataframe["HTGM1"]
        # train_dataframe['ATGM2'] = train_dataframe["HTGM2"]
        # train_dataframe['GP1'] = train_dataframe["HTGP1"]
        # train_dataframe['GP2'] = train_dataframe["HTGP2"]
        
        ########## golurile marcate si golurile primite le tratam ca time series
        train_dataframe["HTGM"]=train_dataframe["HTGM1"]+train_dataframe["HTGM2"]
        train_dataframe["HTGP"]=train_dataframe["HTGP1"]+train_dataframe["HTGP2"]
        train_dataframe["ATGM"]=train_dataframe["ATGM1"]+train_dataframe["ATGM2"]
        train_dataframe["ATGP"]=train_dataframe["ATGP1"]+train_dataframe["ATGP2"]
        
        train_dataframe["HTGM3"] = train_dataframe["HTGM"].diff().rolling(3).mean()
        train_dataframe["HTGP3"] = train_dataframe["HTGP"].diff().rolling(3).mean()
        train_dataframe["ATGM3"] = train_dataframe["ATGM"].diff().rolling(3).mean()
        train_dataframe["ATGP3"] = train_dataframe["ATGP"].diff().rolling(3).mean()
        
        
        # train_dataframe['COEF1'] = train_dataframe["HTCOEF1"] + train_dataframe["HTCOEF2"]
        # train_dataframe['COEF2'] = train_dataframe["HTCOEF1"] 
        train_dataframe['ATRANKING'] =train_dataframe["ATRANKING"]+4
        # train_dataframe['HTPOINTS'] = train_dataframe["HTPOINTS"]/(train_dataframe["HTPLAYED1"] + train_dataframe["HTPLAYED2"]+1) 
        # train_dataframe['ATPOINTS'] = train_dataframe["ATPOINTS"]/(train_dataframe["ATPLAYED1"] + train_dataframe["ATPLAYED2"]+1)
        # train_dataframe["COEF3"] = train_dataframe["ATCOEF1"] + train_dataframe["ATCOEF2"]
        # train_dataframe["COEF4"] = train_dataframe["ATCOEF2"]
        # train_dataframe['RANKING'] = train_dataframe['RANKING']/2

        train_dataframe = train_dataframe[coloane]
        
        train_dataframe = train_dataframe[train_dataframe.FTR != -1]
        self.ytrain = train_dataframe["FTR"]
        # self.ytrain_is_surprise= train_dataframe["IS_NORMAL_RESULT"]
        self.xtrain = train_dataframe.drop(["FTR"], axis=1)

        
        ## x_test si y_test ###############################################################################################################

        test_dataframe["country_cat"] = (
            test_dataframe["country"].astype("category").cat.codes
        )
        test_dataframe["divizia_cat"] = (
            test_dataframe["divizia"].astype("category").cat.codes
        )
        # test_dataframe["dif"] = (
        #     test_dataframe["PlaceHome"] - test_dataframe["PlaceAway"]
        # )
        
        test_dataframe["HomeTeamCat"] = test_dataframe["HomeTeam"].astype("category").cat.codes
        test_dataframe["AwayTeamCat"] = test_dataframe["AwayTeam"].astype("category").cat.codes

        # test_dataframe['GM1'] = test_dataframe["HTGM1"]
        # test_dataframe['GM2'] = test_dataframe["HTGM2"]
        # test_dataframe['GP1'] = test_dataframe["HTGP1"]
        # test_dataframe['GP2'] = test_dataframe["HTGP2"]
 
        ########## golurile marcate si golurile primite le tratam ca time series
        test_dataframe["HTGM"]=test_dataframe["HTGM1"]+test_dataframe["HTGM2"]
        test_dataframe["HTGP"]=test_dataframe["HTGP1"]+test_dataframe["HTGP2"]
        test_dataframe["ATGM"]=test_dataframe["ATGM1"]+test_dataframe["ATGM2"]
        test_dataframe["ATGP"]=test_dataframe["ATGP1"]+test_dataframe["ATGP2"]
        
        test_dataframe["HTGM3"] = test_dataframe["HTGM"].diff().rolling(3).mean()
        test_dataframe["HTGP3"] = test_dataframe["HTGP"].diff().rolling(3).mean()
        test_dataframe["ATGM3"] = test_dataframe["ATGM"].diff().rolling(3).mean()
        test_dataframe["ATGP3"] = test_dataframe["ATGP"].diff().rolling(3).mean()
        ###########################################################################
        
        # test_dataframe['COEF1'] = test_dataframe["HTCOEF1"] + test_dataframe['HTCOEF2']
        # test_dataframe['COEF2'] = test_dataframe["HTCOEF1"]
        test_dataframe['ATRANKING'] =test_dataframe["ATRANKING"]+4
        # test_dataframe['HTPOINTS'] = test_dataframe["HTPOINTS"] / (test_dataframe["HTPLAYED1"] + test_dataframe["HTPLAYED2"]+1)
        # test_dataframe['ATPOINTS'] = test_dataframe["ATPOINTS"] / (test_dataframe["ATPLAYED1"]+ test_dataframe['ATPLAYED2']+1)
        
        # test_dataframe["COEF3"] = test_dataframe["ATCOEF1"]+test_dataframe['ATCOEF2']
        # test_dataframe["COEF4"] = test_dataframe["ATCOEF2"]
        # test_dataframe['RANKING'] = test_dataframe['RANKING']/2

        test_dataframe = test_dataframe[coloane]
        
        test_dataframe = test_dataframe[test_dataframe.FTR != -1]
        self.test_dataframe_full = self.test_dataframe_full[self.test_dataframe_full.FTR != -1]
        self.ytest = test_dataframe["FTR"]
        # self.ytest_is_surprise= test_dataframe["IS_NORMAL_RESULT"]
        self.xtest = test_dataframe.drop(["FTR"], axis=1)


       
        ######### X TEST pentru cele nejucate
        test_dataframe_unplayed["country_cat"] = (
            test_dataframe_unplayed["country"].astype("category").cat.codes
        )
        test_dataframe_unplayed["divizia_cat"] = (
            test_dataframe_unplayed["divizia"].astype("category").cat.codes
        )
        # test_dataframe_unplayed["dif"] = (
        #     test_dataframe_unplayed["HTRANKING"] - train_dataframe["ATRANKING"]
        # )
        
        ########## golurile marcate si golurile primite le tratam ca time series
        test_dataframe_unplayed["HTGM"]=test_dataframe_unplayed["HTGM1"]+test_dataframe_unplayed["HTGM2"]
        test_dataframe_unplayed["HTGP"]=test_dataframe_unplayed["HTGP1"]+test_dataframe_unplayed["HTGP2"]
        test_dataframe_unplayed["ATGM"]=test_dataframe_unplayed["ATGM1"]+test_dataframe_unplayed["ATGM2"]
        test_dataframe_unplayed["ATGP"]=test_dataframe_unplayed["ATGP1"]+test_dataframe_unplayed["ATGP2"]
        
        test_dataframe_unplayed["HTGM3"] = test_dataframe_unplayed["HTGM"].diff().rolling(3).mean()
        test_dataframe_unplayed["HTGP3"] = test_dataframe_unplayed["HTGP"].diff().rolling(3).mean()
        test_dataframe_unplayed["ATGM3"] = test_dataframe_unplayed["ATGM"].diff().rolling(3).mean()
        test_dataframe_unplayed["ATGP3"] = test_dataframe_unplayed["ATGP"].diff().rolling(3).mean()
        ###########################################################################
        
        test_dataframe_unplayed["HomeTeamCat"] = test_dataframe_unplayed["HomeTeam"].astype("category").cat.codes
        test_dataframe_unplayed["AwayTeamCat"] = test_dataframe_unplayed["AwayTeam"].astype("category").cat.codes
        # test_dataframe_unplayed['GM1'] = test_dataframe_unplayed["HTGM1"]/test_dataframe_unplayed["HTPLAYED1"]
        # test_dataframe_unplayed['GM2'] = test_dataframe_unplayed["HTGM2"]/test_dataframe_unplayed["HTPLAYED2"]
        # test_dataframe_unplayed['GP1'] = test_dataframe_unplayed["HTGP1"]/test_dataframe_unplayed["HTPLAYED1"]
        # test_dataframe_unplayed['GP2'] = test_dataframe_unplayed["HTGP2"]/test_dataframe_unplayed["HTPLAYED2"]
        # test_dataframe_unplayed['COEF1'] = test_dataframe_unplayed["HTCOEF1"] + test_dataframe_unplayed['HTCOEF2']
        # test_dataframe_unplayed['COEF2'] = test_dataframe_unplayed["HTCOEF1"]
        test_dataframe_unplayed['ATRANKING'] =test_dataframe_unplayed["ATRANKING"]+4
        # test_dataframe_unplayed['HTPOINTS'] = \
        # test_dataframe_unplayed["HTPOINTS"]/(test_dataframe_unplayed["HTPLAYED1"] + test_dataframe_unplayed["HTPLAYED2"]+1)
        # test_dataframe_unplayed["ATPOINTS"] = test_dataframe_unplayed['ATPOINTS']/(test_dataframe_unplayed["ATPLAYED1"] + test_dataframe_unplayed["ATPLAYED2"]+1)

        # test_dataframe_unplayed["COEF3"] = test_dataframe_unplayed["ATCOEF1"] + test_dataframe_unplayed["ATCOEF2"]
        # test_dataframe_unplayed["COEF4"] = test_dataframe_unplayed["ATCOEF2"]
        # test_dataframe_unplayed['RANKING'] = test_dataframe_unplayed['RANKING']/2

        
        test_dataframe_unplayed = test_dataframe_unplayed[coloane]
        
        self.ytest_unplayed = test_dataframe_unplayed["FTR"]            
        # self.ytest_is_surprise_unplayed= test_dataframe_unplayed["IS_NORMAL_RESULT"]
        self.test_dataframe_unplayed = test_dataframe_unplayed.drop(["FTR"], axis=1)
        self.scaler = MinMaxScaler(feature_range=(0,1))

    def GetXTrain(self):
        return pd.DataFrame(self.xtrain)
    
    def GetXTrainScaled(self):
        return self.scaler.fit_transform(self.xtrain)
    
    # testare
    def GetXTest(self):
        return self.xtest
    
    #pentru afisare predictie
    def GetXTestFull(self):
        return self.test_dataframe_full
    
    # def GetXTestScaled(self):
    #     return self.scaler.fit_transform(self.xtest)
      
    def GetYTrain(self):
        return self.ytrain
    
    # def GetYTrainScaled(self):
    #     return self.scaler.fit_transform(np.array(self.ytrain).reshape(-1,1))
        
    def GetYTest(self):
        return self.ytest
    
    # def GetYTestIsSurprise(self):
    #     return self.ytest_is_surprise
    
    # def GetYTrainIsSurprise(self):
    #     return self.ytrain_is_surprise
    
    def GetYTestUnplayed(self):
        return self.ytest_unplayed
    
    def GetYTestScaled(self):
        return self.scaler.fit_transform(np.array(self.ytest).reshape(-1,1))
    

    ##### cel cu care calculez predictia
    def GetXTestUnplayed(self):
        return self.test_dataframe_unplayed

    ##### cel cu care afisez predictia
    def GetXTestUnplayedFull(self):
        return self.test_dataframe_unplayed_full




