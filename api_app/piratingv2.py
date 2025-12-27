import mysql.connector
import pandas as pd
import numpy as np
import math

def get_pi_ratings_and_update(df, params, my_cursor):
    """
    Calculează Pi-ratings și actualizează direct tabela 'games' cu valorile
    pentru fiecare meci.
    
    df: DataFrame cu coloane ['id','ts','Home Team','Away Team','FTHG','FTAG']
    params: (c, mu1, mu2)
    db_conn: conexiune mysql.connector.connect(...)
    """

    # ordine cronologică
    # df = df.sort_values(by='ts', ascending=True).reset_index(drop=True)

    # echipe și inițializare ratinguri
    keys = list(set(list(df['HomeTeam']) + list(df['AwayTeam'])))
    pi_dict = {f"Home {k}": 0.0 for k in keys}
    pi_dict.update({f"Away {k}": 0.0 for k in keys})

    c, mu1, mu2 = params
    home_key, away_key = 'Home {}', 'Away {}'

    # cursor = db_conn.cursor()

    def exp_goal_diff(c, hr, ar):
        egda = (10**(abs(ar)/c) - 1)
        egda = -egda if ar < 0 else egda
        egdh = (10**(abs(hr)/c) - 1)
        egdh = -egdh if hr < 0 else egdh
        return egdh - egda

    def get_error(obs, exp):
        return abs(obs - exp)

    def get_weighted_error(c, error, obs, exp):
        if exp < obs:
            we1 =  c * np.log10((1+error))
            we2 = -we1
        else:
            we1 = -(c * np.log10((1+error)))
            we2 = -we1
        return we1, we2

    def update_ratings(wehome, weaway, hrhome, hraway, arhome, araway, mu1, mu2):
        hrhome_new = hrhome + (wehome * mu1)
        hraway_new = hrhome + (hrhome_new - hrhome) * mu2
        araway_new = araway + (weaway * mu1)
        arhome_new = arhome + (araway_new - araway) * mu2
        return hrhome_new, hraway_new, arhome_new, araway_new

    for _, row in df.iterrows():
        match_id = row['id']
        home, away = row['HomeTeam'], row['AwayTeam']
        home_score, away_score = int(row['FTHG']), int(row['FTAG'])

        h_hr = pi_dict[home_key.format(home)]
        h_ar = pi_dict[away_key.format(home)]
        a_hr = pi_dict[home_key.format(away)]
        a_ar = pi_dict[away_key.format(away)]

        egd = exp_goal_diff(c, h_hr, a_ar)
        obs_goals = home_score - away_score
        error = get_error(obs_goals, egd)
        wehome, weaway = get_weighted_error(c, error, obs_goals, egd)
        pi_diff = h_hr - a_ar

        h_hr_new, h_ar_new, a_hr_new, a_ar_new = update_ratings(
            wehome, weaway, h_hr, h_ar, a_hr, a_ar, mu1, mu2
        )

        pi_dict[home_key.format(home)] = h_hr_new
        pi_dict[away_key.format(home)] = h_ar_new
        pi_dict[home_key.format(away)] = a_hr_new
        pi_dict[away_key.format(away)] = a_ar_new

        # ---- update direct în baza de date ----
        sql = "UPDATE games  SET hpirating1  = %s, hpirating2  = %s, \
            apirating1  = %s, apirating2  = %s  WHERE id = %s"
        
        values = (float(h_hr), float(h_ar), float(a_hr), float(a_ar), match_id)
        my_cursor.execute(sql, values)

    # db_conn.commit()
    # cursor.close()
    print("Pi-ratings actualizate în tabelul games.")
    
    


# # extragem meciurile
# df = pd.read_sql("SELECT id, dataj as ts, HomeTeam as `Home Team`, AwayTeam as `Away Team`, FTHG, FTAG FROM games ORDER BY dataj ASC", mydb)





###===================================================================================================================================================
# ---- Conectare la MySQL și citire meciuri ----
mydb = mysql.connector.connect(user='ai', password='sda',
                              host='127.0.0.1',
                              database='soccer_analysis',
                              auth_plugin='mysql_native_password')
mycursor = mydb.cursor(dictionary=True)

mycursor.execute("select distinct country, league_name  from leagues")
#mycursor.execute("select distinct country, league_name, sezon1,sezon2 from leagues where download=1")
sezoane = mycursor.fetchall()
for sezon in sezoane:
    
    sql = f"SELECT id, dataj, HomeTeam, AwayTeam, FTHG, FTAG FROM games where country='{sezon['country']}' and divizia='{sezon['league_name']}' ORDER BY dataj ASC"
    df = pd.read_sql(sql, mydb)

    # parametri (aleși după literatură sau grid-search)
    params = (10.0, 0.06, 0.6)

    # rulează și actualizează
    get_pi_ratings_and_update(df, params, mycursor)


    # # ---- Calculează Pi-ratings ----
    # r_home, r_away, hist = compute_pi_ratings(df, lambda_=0.06, gamma=0.6)

    # # ---- Scrie ratingurile în DB (opțional) ----
    # for _, row in hist.iterrows():
    #     query = "UPDATE games  SET hpirating1 = %s, hpirating2 = %s, apirating1 = %s , apirating2 = %s  WHERE id = %s "
    #     mycursor.execute(query, (row["home_rating_before1"], row["home_rating_before2"], row["away_rating_before1"], row["away_rating_before2"], row["match_id"]))

    mydb.commit()
mycursor.close()
mydb.close()

print("Ratings Pi actualizate pentru echipe.")