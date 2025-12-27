<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" href="css/mycss.css">
</head>

</head>
<body>
<h1 align='center'>Lista meciurilor urmatoare</h1>

<?php
$servername = "my_bet_db";
$username = "sda";
$password = "sda";
$dbname = "soccer_analysis";
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) 
  {
  die("Connection Failed" . $conn->connect_error);
}

//descarca meciurile toate meciurile din liga

//proceseaza meciurile complete:
// verifica daca este in baza de date: tara, liga, gazde, oaspeti, completed
//daca este in baza de date repune cotele si scorul final

//proceseaza meciurile incomplete
//verifica daca este in baza de date: tara,liga,gazde,oaspeti,completed
//daca este in baza de date nu mai adaug, altfel adaug

$query = "select * from  leagues where  download=1";
$result = mysqli_query($conn, $query);

$nr_new_incompleted  = 0;
$nr_new_completed    = 0;

$arr_new_incomplete = [];
$arr_new_completed  = [];

$nrcrt=0;
while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) 
  {
  $country      = $row['country'];  
  $league_id    = $row['league_id'];
  $league_name  = $row['league_name'];
  $nrcrt++;
  //ob_flush();
  flush();
  $sezon1       = $row['sezon1'];
  $sezon2       = $row['sezon2'];
  //footystats.org/premium?refer=<hohagigi></hohagigi>                54eafef24f9884e1f5ba5a23ced7a8a74cf858378172bee8abc4698cf8e6d73a
  $string_url = "https://api.football-data-api.com/league-matches?key=54eafef24f9884e1f5ba5a23ced7a8a74cf858378172bee8abc4698cf8e6d73a&season_id=".$league_id;
  $result1 = file_get_contents($string_url);
  $result1 = json_decode($result1, true);
  $matches = $result1['data'];
  echo $nrcrt." Processing league: <strong>" .htmlspecialchars($country)." ".htmlspecialchars($league_name) . "</strong> ID league:".$row['league_id']."<br>";
  //echo $matches;
  foreach($matches as $match)
    {  
    //print ($match['home_name']." ".$match['away_name']." ");
     $homeTeamName=str_replace("'","",$match['home_name']);
     $awayTeamName=str_replace("'","",$match['away_name']);
         //  se descarca un meci incomplet si cotele sunt zero => meciul se va disputa intr=o perioada mai indepartata
    // continui cu urmatoarea inregistrare
    //meciul se joaca in viitorul indepartat
    if($match['status']=="incomplete" && $match['odds_ft_1']==0)      continue;

    //caut meciul in BD
    $sql_match = "select * from games where HomeTeam='".$homeTeamName."' and AwayTeam='".$awayTeamName."' 
        and sezon1=".$row['sezon1']." and sezon2  = ".$row['sezon2']." 
        and divizia='".$row['league_name']."'";
    $result_match = mysqli_query($conn, $sql_match);
    //print $sql_match;
    $row_match = mysqli_fetch_array($result_match, MYSQLI_ASSOC);

    $numar_inregistrari = mysqli_num_rows($result_match);
    //print ($numar_inregistrari." ");
    //daca il gasesc suspendat ii modific statusul in baza de date
    if($numar_inregistrari==1 && $match['status']=="suspended")
        {
        //update rez final, cotele, status
        $sql_upd = "update games set status='".$match['status']."' where id=".$row_match['id'];
        //print ($sql_upd);
        if (!mysqli_query($conn,$sql_upd))    mysqli_errno($conn);
          else
          {
          $nr_new_completed++;
          //print ($match['home_name']." ".$match['away_name']);
          }
        }        

      // daca meciul este in viitorul apropiat si are cotele introduse
    if ($match['status']=="incomplete" && $match['odds_ft_1']>0)
      {  
       //daca nu il gasesc il adaug
        if($numar_inregistrari == 0)
            {
            $sql_ins = "insert into games 
              (country,divizia,dataj,sezon1,sezon2,status,HomeTeam,AwayTeam,FTHG,FTAG,FTR,B365H,B365D,B365A)
                values 
              ('".$row['country']."','".$row['league_name']."','".date("Y-m-d H:i:s",$match['date_unix'])."',
              ".$row['sezon1'].",".$row['sezon2'].",'".$match['status']."','".$homeTeamName."','".$awayTeamName."',
              -1,-1,-1,".$match['odds_ft_1'].",".$match['odds_ft_x'].",".$match['odds_ft_2'].")";
              //print $sql_ins;
            if (!mysqli_query($conn,$sql_ins))    mysqli_errno($$conn);
            else {
              $nr_new_incompleted ++;
                 }
            }
        

        // daca il gasesc de doua sau de mai multe ori
        if($numar_inregistrari>1)
        {
                  print ("Inconsistenta logica! Exista mai mult de un meci in BD ... mai mult ca sigur am introdus EU de doua ori");
                  //print ($match['home_name']);
        }

        //daca mai este deja in DATASET, actualizez ora de desfasurare si cotele
        if($numar_inregistrari==1 && $row_match['status']=="incomplete")
            {
              $sql_upd = "update games set dataj='".date("Y-m-d H:i:s",$match['date_unix'])."', B365H=".$match['odds_ft_1'].
                  ",B365D=".$match['odds_ft_x'].
                  ",B365A=".$match['odds_ft_2']." where id=".$row_match['id'];
                  //print ($sql_upd);
                  if (!mysqli_query($conn,$sql_upd))    mysqli_errno($conn);
                  else
                  {

                  }
            }


        //daca il gasesc "completed"  am o problema de inconsistenta si logica din partea dataset owner:))
        if($numar_inregistrari==1 && $row_match['status']=="complete")
                  print ("Inconsistenta majora in dataset !!!!".$match['home_name']." ".$match['away_name']);
             
      }
/////////////////////////////////////////////////////////////////////////////////////////


    if($match['status']=="complete")
      {
        //print ($sql_match);

        $ftr=-1;
        if($match['homeGoalCount']> $match['awayGoalCount']) $ftr=0;
        if($match['homeGoalCount']==$match['awayGoalCount']) $ftr=1;
        if($match['homeGoalCount']< $match['awayGoalCount']) $ftr=2;  
        //daca gasesc mai mult de un rand atunci e un caz de inconsistenta
        if($numar_inregistrari>1)
        {
                  //print ("Inconsistenta logica! Exista mai mult de un meci in BD ... mai mult ca sigur am introdus EU de doua ori");
                  //print ($match['home_name']);
         }
    
        //daca nu il gasesc , il adaug (e cazul cand dau update rar , la peste o saptmana)
        if($numar_inregistrari == 0)
                {
              
                $sql_ins = "insert into games 
                  (country,divizia,dataj,sezon1,sezon2,status,HomeTeam,AwayTeam,FTHG,FTAG,FTR,B365H,B365D,B365A)
                    values 
                  ('".$row['country']."','".$row['league_name']."','".date("Y-m-d H:i:s",$match['date_unix'])."',
                  ".$row['sezon1'].",".$row['sezon2'].",'".$match['status']."','".$homeTeamName."','".$awayTeamName."',
                  ".$match['homeGoalCount'].",".$match['awayGoalCount'].",".$ftr.",".$match['odds_ft_1'].",".$match['odds_ft_x'].",".$match['odds_ft_2'].")";
                  //print ($sql_ins);
                  if (!mysqli_query($conn,$sql_ins))        mysqli_errno($$conn);
                  else    $nr_new_completed ++;
                }


            /////////////// daca am gasit exact o inregistrare ...    

        //daca il gasesc incomplet ii modific rez final , cotele , scorul si statusul
        if($numar_inregistrari==1 && $row_match['status']=="incomplete")
                {
                  //update rez final, cotele, status
                $sql_upd = "update games set FTHG=".$match['homeGoalCount'].",FTAG=".$match['awayGoalCount'].",
                  FTR=".$ftr.", B365H=".$match['odds_ft_1'].",B365D=".$match['odds_ft_x'].",
                  B365A=".$match['odds_ft_2'].",status='".$match['status']."' where id=".$row_match['id'];
                  //print ($sql_upd);
                  if (!mysqli_query($conn,$sql_upd))    mysqli_errno($conn);
                  else
                  {
                    $nr_new_completed++;
                                //print ($match['home_name']." ".$match['away_name']);
                  }
                }
        
        
        
        //daca il gasesc complete atunci continui

        if($numar_inregistrari==1 && $row_match['status']=="complete")
        {
           $sql_upd = "update games set HT_SHOTSONTARGET=".($match['team_a_shotsOnTarget']+0).",AT_SHOTSONTARGET=".($match['team_b_shotsOnTarget']+0).",
                  HT_SHOTSOFFTARGET=".($match['team_a_shotsOffTarget']+0).",AT_SHOTSOFFTARGET=".($match['team_b_shotsOffTarget']+0).",
                  HT_FOULS=".($match['team_a_fouls']+0).",AT_FOULS=".($match['team_b_fouls']+0).",
                  HT_POSSESSION=".($match['team_a_possession']+0).",AT_POSSESSION=".($match['team_b_possession']+0).",
                  HT_DANGEROUSATTACKS=".($match['team_a_dangerous_attacks']+0).",AT_DANGEROUSATTACKS=".($match['team_b_dangerous_attacks']+0).",
                  HT_ATTACKS=".($match['team_a_attacks']+0).",AT_ATTACKS=".($match['team_b_attacks']+0).",
                  HT_CORNERS=".($match['team_a_corners']+0).",AT_CORNERS=".($match['team_b_corners']+0).",
                  HT_OFFSIDES=".($match['team_a_offsides']+0).",AT_OFFSIDES=".($match['team_b_offsides']+0)." where id=".$row_match['id'];
                  //print ($sql_upd);
                  mysqli_query($conn,$sql_upd);
        }         
      }  

    }   //end foreach
  }   //end while
    
print ("<h3> Au fost adaugate ".$nr_new_incompleted." meciuri care urmeaza sa se joace / 
              Au fost adaugate ".$nr_new_completed." meciuri care s-au jucat</h3>");

/*
$query = "select * from  games where  status='incomplete' order by dataj asc";
$result = mysqli_query($conn, $query);
$class = "tdClass";
print "<table style='margin: 0px auto;align=center'>";
print "<tr  class='aTabletr'>";
print "<td class='" . $class . "' align-'center'></td>";
print "<td class='" . $class . "'>Tara<br>Liga</td>";
print "<td class='" . $class . "' align='center'>Data</td>";
print "<td class='" . $class . "'>Gazde</td>";
print "<td class='" . $class . "'>Oaspeti</td>";
print "<td class='" . $class . "'>1</td>";
print "<td class='" . $class . "'>x</td>";
print "<td class='" . $class . "'>2</td>";
print "<td class='" . $class . "'>Etapa</td>";
print "<td class='" . $class . "'>Goluti<br>marcate</td>";
print "<td class='" . $class . "'>Goluri<br>primite<br>Home<br>Team</td>";
print "<td class='" . $class . "'>Goluri<br>marcate</td>";
print "<td class='" . $class . "'>Goluri<br>primite</td>";
print "<td class='" . $class . "'>Loc<br>gazde</td>";
print "<td class='" . $class . "'>Loc<br>oaspeti</td>";
print "<td class='" . $class . "'>Coef<br>Gazde</td>";
print "<td class='" . $class . "'>Coef<br>Oaspeti</td>";
print "<td class='" . $class . "'>Pred 1<br>(league)</td>";
print "<td class='" . $class . "'>Pred 1<br>(league)</td>";
print "<td class='" . $class . "'>Pred X<br>(league)</td>";
print "<td class='" . $class . "'>Pred 2<br>(league)</td>";
print "<td class='" . $class . "'>Pred 2<br>(all)</td>";
print "<td class='" . $class . "'>Pred 1<br>(all)</td>";
print "<td class='" . $class . "'>Pred X<br>(all)</td>";
print "<td class='" . $class . "'>Pred 2<br>(all)</td>";
print "<td class='" . $class . "'>Pred DT<br>(all)</td>";
print "<td class='" . $class . "'>Pred XGB<br>(all)</td>";


print "</tr>";
$i = 1;
while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) 
  {
  $class = "tdClass";
  print "<tr  class='aTabletr'>";
  print "<td class='" . $class . "'>" . $i . "</td>";
  print "<td class='" . $class . "' align='left'>" . $row['country'] ." ".$row['divizia']."</td>";
  print "<td class='" . $class . "' align='center'>" . substr($row['dataj'],0,16) . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HomeTeam'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['AwayTeam'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['B365H'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['B365D'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['B365A'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['MatchDay'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HTGM'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HTGP'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATGM'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATGP'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['PlaceHome'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['PlaceAway'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['LastGamesHome'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['LastGamesAway'] . "</td>";
  if($row['pred1']==0)
    {
    print "<td class='tdClass0'>" . $row['pred1'] . "</td>";
    print "<td class='tdClass0'>" . $row['pred1_1'] . "</td>";
    print "<td class='tdClass0'>" . $row['pred1_x'] . "</td>";
    print "<td class='tdClass0' align='center'>" . $row['pred1_2'] . "</td>";
    }
 if($row['pred1']==1)
    {
    print "<td class='tdClass1'>" . $row['pred1'] . "</td>";
    print "<td class='tdClass1'>" . $row['pred1_1'] . "</td>";
    print "<td class='tdClass1'>" . $row['pred1_x'] . "</td>";
    print "<td class='tdClass1' align='center'>" . $row['pred1_2'] . "</td>";
    }
  if($row['pred1']==2)
    {
    print "<td class='tdClass2'>" . $row['pred1'] . "</td>";
    print "<td class='tdClass2'>" . $row['pred1_1'] . "</td>";
    print "<td class='tdClass2'>" . $row['pred1_x'] . "</td>";
    print "<td class='tdClass2' align='center'>" . $row['pred1_2'] . "</td>";
    }
    if($row['pred2']==0)
    {
    print "<td class='tdClass0'>" . $row['pred2'] . "</td>";
    print "<td class='tdClass0'>" . $row['pred2_1'] . "</td>";
    print "<td class='tdClass0'>" . $row['pred2_x'] . "</td>";
    print "<td class='tdClass0' align='center'>" . $row['pred2_2'] . "</td>";
    }
 if($row['pred2']==1)
    {
    print "<td class='tdClass1'>" . $row['pred2'] . "</td>";
    print "<td class='tdClass1'>" . $row['pred2_1'] . "</td>";
    print "<td class='tdClass1'>" . $row['pred2_x'] . "</td>";
    print "<td class='tdClass1' align='center'>" . $row['pred2_2'] . "</td>";
    }
  if($row['pred2']==2)
    {
    print "<td class='tdClass2'>" . $row['pred2'] . "</td>";
    print "<td class='tdClass2'>" . $row['pred2_1'] . "</td>";
    print "<td class='tdClass2'>" . $row['pred2_x'] . "</td>";
    print "<td class='tdClass2' align='center'>" . $row['pred2_2'] . "</td>";
    }      
    $name_of_class = "tdClass".$row['predDT'];
  print "<td class='".$name_of_class."'>" . $row['predDT'] . "</td>";
    
  $name_of_class = "tdClass".$row['predXGB'];
  print "<td class='".$name_of_class."'>" . $row['predXGB'] . "</td>";

  $i++;
  print "</tr>";
}
print "</table>";

*/
?>
</body>
</html>