import mysql.connector
import pandas as pd
from collections import defaultdict
import numpy as np
import math

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

    # ---- Calculează Pi-ratings ----
    r_home, r_away, hist = compute_pi_ratings(df, lambda_=0.06, gamma=0.6)

    # ---- Scrie ratingurile în DB (opțional) ----
    for _, row in hist.iterrows():
        query = "UPDATE games  SET hpirating1 = %s, hpirating2 = %s, apirating1 = %s , apirating2 = %s  WHERE id = %s "
        mycursor.execute(query, (row["home_rating_before1"], row["home_rating_before2"], row["away_rating_before1"], row["away_rating_before2"], row["match_id"]))

    mydb.commit()
mycursor.close()
mydb.close()

print("Ratings Pi actualizate pentru echipe.")

