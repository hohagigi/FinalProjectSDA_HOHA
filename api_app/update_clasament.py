
import mysql.connector
from datetime import datetime


def completeaza_coloane_clasament(mycursor):
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

start_time = datetime.now()
mydb = mysql.connector.connect(user='ai', password='sda',
                              host='127.0.0.1',
                              database='soccer_analysis',
                              auth_plugin='mysql_native_password')
mycursor = mydb.cursor(dictionary=True)
  
mycursor.execute("select count(*) as count from  games")    
x=mycursor.fetchone()
numar_total_inregistrari=x['count']
  
print ("\r Numar inreg: ",numar_total_inregistrari,end='')
    ##time.sleep(0.000001)

completeaza_coloane_clasament(mycursor)

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))


## toate ligile 22 secunde
## doar ligile cu download 2 secunde