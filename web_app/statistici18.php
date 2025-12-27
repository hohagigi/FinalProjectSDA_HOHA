<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" href="css/mycss.css?v=1.0">
</head>
<style>

</style>
<h4 align='center'>Precizia predictiilor (pe fiecare liga in parte/pe fiecare tip de rezultat/ over all )</h4>

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

if (isset($_GET["data_inceput"])) $data_inceput=$_GET["data_inceput"];
else $data_inceput=date("Y-m-d");

if (isset($_GET["data_sfarsit"])) $data_sfarsit=$_GET["data_sfarsit"];
else $data_sfarsit=date("Y-m-d");

if(isset($_GET["castigator"])) $castigator=$_GET["castigator"];
else $castigator=1;

if(isset($_GET["suma"])) $miza=$_GET["miza"];
else $miza=10;

if(isset($_GET["sortare_dupa_data"])) $sortare_dupa_data=$_GET["sortare_dupa_data"];
else $sortare_dupa_data=0;

if(isset($_GET["sortare_dupa_liga"])) $sortare_dupa_liga=$_GET["sortare_dupa_liga"];
else $sortare_dupa_liga=0;

if(isset($_GET["liga"]))  $liga=$_GET["liga"];
else $liga="toate";

if(isset($_GET["tip_pred"]))  $tip_pred=$_GET["tip_pred"];
else $tip_pred="pred2";

?>

  <form method="GET" name="criterii">
    <table style="  border: 0px solid black;" align="center">
      <tr>
          <td>
              <table>
                <tr>
                  <td class='tdClassSelect'>
                    <input type="date" value="<?php print ($data_inceput); ?>" name="data_inceput">
                  </td>
                </tr>
                <tr>
                  <td class='tdClassSelect'>
                    <input type="date" value="<?php print ($data_sfarsit); ?>" name="data_sfarsit">
                  </td>
                </tr>
              </table>                  
          </td>
          <td>
              <table>
                <tr>
                  <td class='tdClassSelect' style="text-align:left;">
                    <input type="radio" id="id_gazde" name="castigator" value="0" <?php if ($castigator==0) print ("checked")  ?>>
                    <label for="id_gazde">gazde</label>
                  </td>
                </tr>

               <tr>
                  <td class='tdClassSelect' style="text-align:left;">
                    <input type="radio" id="id_oaspeti" name="castigator" value="2" <?php if ($castigator==2) print ("checked")  ?> >
                    <label for="id_egalitate">oaspeti</label>
                  </td>
                </tr> 
                <tr>
                  <td class='tdClassSelect' style="text-align:left;">
                    <input type="radio" id="id_egalitate" name="castigator" value="1" <?php if ($castigator==1) print ("checked")  ?> >
                    <label for="id_egalitate">H + A</label>
                  </td>
                </tr>                
              </table>         
          </td>

          <td>
              <table>
                <tr>
                  <td class='tdClassSelect' style="text-align:left;">
                    <input type="text" id="id_suma" name="miza" value="<?php  print ($miza);  ?>"  >
               
                  </td>
                </tr>
                <tr>
                  <td class='tdClassSelect' style="text-align:left;">
                    &nbsp;
                    
                  </td>
                </tr>
              </table>         
          </td>

          <td>
              <table>
                <tr>
                  <td class='tdClassSelect' style="text-align:right;">
                    <label for="id_liga_asc">sortare dupa liga:</label>
                    <label for="id_liga_asc">asc</label>
                    <input type="radio" id="id_liga_asc" name="sortare_dupa_liga" value="0" <?php if ($sortare_dupa_liga==0) print ("checked")  ?>>
                    <label for="id_liga_desc">desc</label>
                    <input type="radio" id="id_liga_desc" name="sortare_dupa_liga" value="1" <?php if ($sortare_dupa_liga==1) print ("checked")  ?> >
                    <label for="id_liga_unst">unsorted</label>
                    <input type="radio" id="id_liga_unst" name="sortare_dupa_liga" value="2" <?php if ($sortare_dupa_liga==2) print ("checked")  ?> >
                  </td>
                </tr>

                <tr>
                  <td class='tdClassSelect' style="text-align:right;">
                    <label for="id_data_asc">sortare dupa data:</label>
                    <label for="id_data_asc">asc</label>
                    <input type="radio" id="id_data_asc" name="sortare_dupa_data" value="0" <?php if ($sortare_dupa_data==0) print ("checked")  ?>  >
                    <label for="id_data_desc">desc</label>
                    <input type="radio" id="id_data_desc" name="sortare_dupa_data" value="1" <?php if ($sortare_dupa_data==1) print ("checked")  ?> >
                    <label for="id_data_unst">unsorted</label>
                    <input type="radio" id="id_data_unst" name="sortare_dupa_data" value="2" <?php if ($sortare_dupa_data==2) print ("checked")  ?> >
                  </td>
                </tr>
              </table>         
          </td>

          <td>
              <table>
                <tr>
                  <td class='tdClassSelect' style="text-align:right;">
                  <label for="liga">Alegeti liga</label>
                  <select name="liga">
                    <option value='toate'>toate</option>
                  <?php
                    $sql_divizia= "select distinct divizia from games";
                    $result_divizia = mysqli_query($conn, $sql_divizia);
                    while ($rowd = mysqli_fetch_array($result_divizia, MYSQLI_ASSOC)) 
                      {
                        if ($rowd['divizia']==$liga)
                          print ("<option value='".$rowd['divizia']."' selected>".$rowd['divizia']."</option><br>");
                        else
                          print ("<option value='".$rowd['divizia']."' >".$rowd['divizia']."</option><br>");
                      }
                  ?>
                  </select>
                  </td>
                </tr>
               <tr>
                  <td class='tdClassSelect' style="text-align:right;">
                  <label for="tip_pred">Alegeti tip predictie</label>
                  <select name="tip_pred">
                  <?php
                                      
                      if ($tip_pred=="pred2") print ("<option value='pred2' selected>Pred (all)</option><br>");
                        else                          print ("<option value='pred2' >Pred (all)</option><br>");
                      
                      if ($tip_pred=="predDT")  print ("<option value='predDT' selected>Pred DT</option><br>");
                        else                            print ("<option value='predDT' >Pred DT</option><br>");
                     
                      if ($tip_pred=="predCB") print ("<option value='predCB' selected>Pred CatBoosts</option><br>");
                        else                            print ("<option value='predCB' >Pred CatBoosts</option><br>");
                      
                  ?>
                  </select>
                  </td>
                </tr>
              </table>         
          </td>
          <td>
              <table>
                <tr>
                  <td class='tdClassSelect'>
                  <input type="submit" value="Afiseaza">
                   
                  </td>
                </tr>
              
              </table>         
          </td>

      </tr>          
    </table>
  <form>

<?php

//construiesc interogarea sql in functie de optiunile selectate
// $query="select * from games where status='complete' and
//       dataj>='".$data_inceput."' and dataj <='".$data_sfarsit." 23:59' and ";
// if ($castigator>=0 && $castigator<=2)
//     $query=$query." and ".$tip_pred."=".$castigator;  //ex: adica pred2==1 

// if($liga!="toate")
//   $query=$query." and divizia='".$liga."' ";

// $query=$query." order by dataj asc";

// if($sortare_dupa_data!=2 || $sortare_dupa_liga!=2)
// $query=$query." order by ";

// if ($sortare_dupa_liga==0)
//     $query=$query." divizia asc";
// if ($sortare_dupa_liga==1)
//     $query=$query." divizia desc";

// if (($sortare_dupa_liga==0 || $sortare_dupa_liga==1) && ($sortare_dupa_data==0 || $sortare_dupa_data==1))
//   $query=$query." , ";

// if ($sortare_dupa_data==0)
//     $query=$query." dataj asc";
// if ($sortare_dupa_data==1)
//     $query=$query." dataj desc";


// $sql= "DROP TEMPORARY TABLE IF EXISTS temp_stats";
// if (mysqli_query($conn,$sql) == FALSE) die("Eroare de stergere temporary table");
// $sql = "CREATE TEMPORARY TABLE temp_stats (
//             id INT AUTO_INCREMENT PRIMARY KEY,
//             id_games INT ,
//             precizia0 FLOAT DEFAULT NULL,
//             precizia1 FLOAT DEFAULT NULL,
//             precizia2 FLOAT DEFAULT NULL,
//             precizia3 FLOAT DEFAULT NULL,
//             precizia4 FLOAT DEFAULT NULL,
//             precizia5 FLOAT DEFAULT NULL,
//             precizia6 FLOAT DEFAULT NULL,
//             precizia7 FLOAT DEFAULT NULL,
//             precizia8 FLOAT DEFAULT NULL,
//             preciziaa0 FLOAT DEFAULT NULL,
//             preciziaa1 FLOAT DEFAULT NULL,
//             preciziaa2 FLOAT DEFAULT NULL,
//             preciziaa3 FLOAT DEFAULT NULL,
//             preciziaa4 FLOAT DEFAULT NULL,
//             preciziaa5 FLOAT DEFAULT NULL,
//             preciziaa6 FLOAT DEFAULT NULL,
//             preciziaa7 FLOAT DEFAULT NULL,
//             preciziaa8 FLOAT DEFAULT NULL,
//             preciziab0 FLOAT DEFAULT NULL,
//             preciziab1 FLOAT DEFAULT NULL,
//             preciziab2 FLOAT DEFAULT NULL,
//             preciziab3 FLOAT DEFAULT NULL,
//             preciziab4 FLOAT DEFAULT NULL,
//             preciziab5 FLOAT DEFAULT NULL,
//             preciziab6 FLOAT DEFAULT NULL,
//             preciziab7 FLOAT DEFAULT NULL,
//             preciziab8 FLOAT DEFAULT NULL,
//             preciziac0 FLOAT DEFAULT NULL,
//             preciziac1 FLOAT DEFAULT NULL,
//             preciziac2 FLOAT DEFAULT NULL,
//             preciziac3 FLOAT DEFAULT NULL,
//             preciziac4 FLOAT DEFAULT NULL,
//             preciziac5 FLOAT DEFAULT NULL,
//             preciziac6 FLOAT DEFAULT NULL,
//             preciziac7 FLOAT DEFAULT NULL,
//             preciziac8 FLOAT DEFAULT NULL
//         )";

// if (mysqli_query($conn,$sql) == FALSE) die("Eroare de creare temporary table");

// $nr_gresite_2 = 0;
// $nr_corecte_2=0;
// $sum_cote2_corecte=0;
// $sum_cote2_gresite=0;

// $nr_gresite_1 = 0;
// $nr_corecte_1=0;
// $sum_cote1_corecte=0;
// $sum_cote1_gresite=0;

// $precizia=array();
// $preciziaa=array(0,0,0,0,0,0,0,0,0);
// $preciziab=array(0,0,0,0,0,0,0,0,0);
// $preciziac=array(0,0,0,0,0,0,0,0,0);

// //print ($query."<br>");
// //$query = "select * from  games where  status='complete' and dataj>'".$data1."' and dataj<'".$data2."' order by dataj asc";
// $result = mysqli_query($conn, $query);
// while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) 
// {
//   if (!array_key_exists($row['country'].$row['divizia'], $precizia)) $precizia[$row['country'].$row['divizia']]=array(0,0,0,0,0,0,0,0,0);
    
//   if($row['FTR']==0 && $row['pred1']==0)   //cea corecta       
//     {
//       $precizia[$row['country'].$row['divizia']][0]++;
//       $sum_cote1_corecte+=$row['B365H'];
//       $nr_corecte_1+=1;
//     }
    
//   if($row['FTR']==1 && $row['pred1']==0)          
//     {
//       $precizia[$row['country'].$row['divizia']][1]++;
//       $sum_cote1_gresite+=$row['B365H'];
//       $nr_gresite_1+=1;
//     }

//   if($row['FTR']==2 && $row['pred1']==0)          
//     {
//       $precizia[$row['country'].$row['divizia']][2]++;
//       $sum_cote1_gresite+=$row['B365H'];
//       $nr_gresite_1+=1;
//     }

//   if($row['FTR']==0 && $row['pred1']==1)          $precizia[$row['country'].$row['divizia']][3]++; 
//   if($row['FTR']==1 && $row['pred1']==1)          $precizia[$row['country'].$row['divizia']][4]++;//cea corecta
//   if($row['FTR']==2 && $row['pred1']==1)          $precizia[$row['country'].$row['divizia']][5]++;

//   if($row['FTR']==0 && $row['pred1']==2)          
//     {
//       $precizia[$row['country'].$row['divizia']][6]++;
//       $sum_cote2_gresite+=$row['B365A'];
//       $nr_gresite_2+=1;
//     } 
//   if($row['FTR']==1 && $row['pred1']==2)          
//       {
//       $precizia[$row['country'].$row['divizia']][7]++;
//       $sum_cote2_gresite+=$row['B365A'];
//       $nr_gresite_2+=1;
//     }    
//   if($row['FTR']==2 && $row['pred1']==2)     //cea corecta     
//       {
//         $precizia[$row['country'].$row['divizia']][8]++;
//         $sum_cote2_corecte+=$row['B365A'];
//         $nr_corecte_2+=1;
//       }

//   if($row['FTR']==0 && $row['pred2']==0)          $preciziaa[0]++; //cea corecta
//   if($row['FTR']==1 && $row['pred2']==0)          $preciziaa[1]++;
//   if($row['FTR']==2 && $row['pred2']==0)          $preciziaa[2]++;
    
//   if($row['FTR']==0 && $row['pred2']==1)          $preciziaa[3]++; 
//   if($row['FTR']==1 && $row['pred2']==1)          $preciziaa[4]++;  //cea corecta
//   if($row['FTR']==2 && $row['pred2']==1)          $preciziaa[5]++;

//   if($row['FTR']==0 && $row['pred2']==2)          $preciziaa[6]++; 
//   if($row['FTR']==1 && $row['pred2']==2)          $preciziaa[7]++;  //cea corecta
//   if($row['FTR']==2 && $row['pred2']==2)          $preciziaa[8]++;
  
//   //// pentru pred DT
//   if($row['FTR']==0 && $row['predDT']==0)          $preciziab[0]++; //cea corecta
//   if($row['FTR']==1 && $row['predDT']==0)          $preciziab[1]++;
//   if($row['FTR']==2 && $row['predDT']==0)          $preciziab[2]++;
    
//   if($row['FTR']==0 && $row['predDT']==1)          $preciziab[3]++; 
//   if($row['FTR']==1 && $row['predDT']==1)          $preciziab[4]++;  //cea corecta
//   if($row['FTR']==2 && $row['predDT']==1)          $preciziab[5]++;

//   if($row['FTR']==0 && $row['predDT']==2)          $preciziab[6]++; 
//   if($row['FTR']==1 && $row['predDT']==2)          $preciziab[7]++;  //cea corecta
//   if($row['FTR']==2 && $row['predDT']==2)          $preciziab[8]++;

// //// pentru pred CatBoosts
//   if($row['FTR']==0 && $row['predXGB']==0)          $preciziac[0]++; //cea corecta
//   if($row['FTR']==1 && $row['predXGB']==0)          $preciziac[1]++;
//   if($row['FTR']==2 && $row['predXGB']==0)          $preciziac[2]++;
    
//   if($row['FTR']==0 && $row['predXGB']==1)          $preciziac[3]++; 
//   if($row['FTR']==1 && $row['predXGB']==1)          $preciziac[4]++;  //cea corecta
//   if($row['FTR']==2 && $row['predXGB']==1)          $preciziac[5]++;

//   if($row['FTR']==0 && $row['predXGB']==2)          $preciziac[6]++; 
//   if($row['FTR']==1 && $row['predXGB']==2)          $preciziac[7]++;  
//   if($row['FTR']==2 && $row['predXGB']==2)          $preciziac[8]++;//cea corecta


//     $sql_insert = " insert into temp_stats (id_games,precizia0,precizia1,precizia2,precizia3,precizia4,precizia5,precizia6,precizia7,precizia8,
//     preciziaa0,preciziaa1,preciziaa2,preciziaa3,preciziaa4,preciziaa5,preciziaa6,preciziaa7,preciziaa8,
//     preciziab0,preciziab1,preciziab2,preciziab3,preciziab4,preciziab5,preciziab6,preciziab7,preciziab8,
//     preciziac0,preciziac1,preciziac2,preciziac3,preciziac4,preciziac5,preciziac6,preciziac7,preciziac8
    
//     )
//     VALUES (".$row['id'].","
//         .$precizia[$row['country'].$row['divizia']][0].",".$precizia[$row['country'].$row['divizia']][1].","
//         .$precizia[$row['country'].$row['divizia']][2].",".$precizia[$row['country'].$row['divizia']][3].","
//         .$precizia[$row['country'].$row['divizia']][4].",".$precizia[$row['country'].$row['divizia']][5].","
//         .$precizia[$row['country'].$row['divizia']][6].",".$precizia[$row['country'].$row['divizia']][7].","
//         .$precizia[$row['country'].$row['divizia']][8].","
//         .$preciziaa[0].",".$preciziaa[1].","
//         .$preciziaa[2].",".$preciziaa[3].","
//         .$preciziaa[4].",".$preciziaa[5].","
//         .$preciziaa[6].",".$preciziaa[7].","
//         .$preciziaa[8].","
//         .$preciziab[0].",".$preciziab[1].","
//         .$preciziab[2].",".$preciziab[3].","
//         .$preciziab[4].",".$preciziab[5].","
//         .$preciziab[6].",".$preciziab[7].","
//         .$preciziab[8].","
//         .$preciziac[0].",".$preciziac[1].","
//         .$preciziac[2].",".$preciziac[3].","
//         .$preciziac[4].",".$preciziac[5].","
//         .$preciziac[6].",".$preciziac[7].","
//         .$preciziac[8].  
//         ") ";
//     if (mysqli_query($conn,$sql_insert) == FALSE) die("Eroare la inserare");    
//     //print $sql_insert."/n";
  
// }
$current_day=date('D', strtotime($data_inceput));
$current_month=date('m', strtotime($current_day));;

$suma_totala=0;
$suma_lunara=0;
$suma_zilnica=0;

$query="select * from  games where  status='complete' and dataj>='".$data_inceput."' and dataj <='".$data_sfarsit." 23:59' ";
if ($castigator>=0 && $castigator<=2)
    $query=$query." and ".$tip_pred."=".$castigator;

if($liga!="toate")
  $query=$query." and divizia='".$liga."' ";

$query=$query." order by dataj asc";

//print ($query);
//$query = "select * from  games, temp_stats where games.id=temp_stats.id_games and  status='complete' and dataj>'".$data1."' and dataj<'".$data2."'  order by dataj desc, games.id desc";
$result = mysqli_query($conn,  $query);
$class = "tdClass";
//print "<h4 style='align:center'>Castigator echipa oaspete: media corecte:".($sum_cote2_corecte/$nr_corecte_2)." media gresite:".(0 if $nr_gresite_2==0 else $sum_cote2_gresite/$nr_gresite_2)."</h4>";
//print "<h4 style='align:center'>Castigator echipa gazda: media corecte:".($sum_cote1_corecte/$nr_corecte_1)." media gresite:".($sum_cote1_gresite/$nr_gresite_1)."</h4>";

print "<table style='margin: 0px auto;align='center'>";
print "<tr  class='aTabletr'>";
print "<td class='" . $class . "' align-'center'></td>";
print "<td class='" . $class . "'>Tara<br>Liga</td>";
print "<td class='" . $class . "' align='center'>Data</td>";
print "<td class='" . $class . "'>Gazde</td>";
print "<td class='" . $class . "'>Oaspeti</td>";
print "<td class='" . $class . "'>Home<br>goal</td>";
print "<td class='" . $class . "'>Away<br>goal</td>";
print "<td class='" . $class . "'>FTR</td>";

print "<td class='" . $class . "'>1</td>";
print "<td class='" . $class . "'>x</td>";
print "<td class='" . $class . "'>2</td>";
print "<td class='" . $class . "'>Pred</td>";
print "<td class='" . $class . "'>Etapa</td>";

print "<td class='" . $class . "'>Loc<br>gazde</td>";
print "<td class='" . $class . "'>Loc<br>oaspeti</td>";

print "<td class='" . $class . "'>Miza</td>";
print "<td class='" . $class . "'>Castig</td>";
print "<td class='" . $class . "'>Sold</td>";

print "<td class='" . $class . "'>Miza</td>";
print "<td class='" . $class . "'>Castig</td>";
print "<td class='" . $class . "'>Sold</td>";


//print "<td class='" . $class . "'>debug<br>(all)</td>";

print "</tr>";
$i = 1;
$sold=100;
$sold_zilnic=100;
$miza_zilnica=$sold/8;
$nr_corecte=0;
$nr_total=0;
while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
  // in caz ca am initializat array nu numele tarii si al ligii pun in array
  $nr_total++;
  $class = "tdClass";
  print "<tr class='trClass'>";
  
  print "<td class='" . $class . "' >" . $i . "</td>";
  print "<td class='" . $class . "' align='left'>" . $row['country'] ." ".$row['divizia']."</td>";
  print "<td class='" . $class . "' align='center'>" . substr($row['dataj'],0,16) . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HomeTeam'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['AwayTeam'] . "</td>";

if($row['FTHG']>$row['FTAG'])
  {
    print "<td class='tdClass0' align='center'>" . $row['FTHG'] . "</td>";
    print "<td class='tdClass0' align='center'>" . $row['FTAG'] . "</td>";
    print "<td class='tdClass0' align='center'>0</td>";
  }

if($row['FTHG']==$row['FTAG'])
  {
    print "<td class='tdClass1' align='center'>" . $row['FTHG'] . "</td>";
    print "<td class='tdClass1 align='center'>" . $row['FTAG'] . "</td>";
    print "<td class='tdClass1' align='center'>1</td>";
  }

if($row['FTHG']<$row['FTAG'])
  {
    print "<td class='tdClass2' align='center'>" . $row['FTHG'] . "</td>";
    print "<td class='tdClass2' align='center'>" . $row['FTAG'] . "</td>";
    print "<td class='tdClass2' align='center'>" . $row['FTR'] . "</td>";
  }

  print "<td class='" . $class . "' align='center'>" . $row['B365H'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['B365D'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['B365A'] . "</td>";



  $miza=$sold/10;
  if ($row['FTR']==$castigator)
    { 
      if ($castigator==0) 
        if ($row['FTR']==0) {$nr_corecte++;$castig=$row['B365H']*$miza;$castig_zilnic=$row['B365H']*$miza_zilnica;}

      if ($castigator==1) 
        if($row['FTR']==1) {$nr_corecte++;$castig=$row['B365D']*$miza;$castig_zilnic=$row['B365D']*$miza_zilnica;}

      if ($castigator==2) 
        if($row['FTR']==2) {$nr_corecte++;$castig=$row['B365A']*$miza;$castig_zilnic=$row['B365A']*$miza_zilnica;}
      
    }
  else
      {$castig=0;$castig_zilnic=0;} 

  $sold= $sold -$miza +$castig;
  $sold_zilnic=$sold_zilnic+$castig_zilnic-$miza_zilnica;
  if($row['FTHG']>$row['FTAG']) print "<td class='tdClass0' align='center'>" . $row['pred2']."(".number_format($nr_corecte*100/$nr_total,1).")</td>";
  if($row['FTHG']==$row['FTAG']) print "<td class='tdClass1' align='center'>" . $row['pred2']."(".number_format($nr_corecte*100/$nr_total,1).")</td>";
  if($row['FTHG']<$row['FTAG']) print "<td class='tdClass2' align='center'>" . $row['pred2']."(".number_format($nr_corecte*100/$nr_total,1).")</td>";
   
  print "<td class='" . $class . "' align='center'>" . $row['MatchDay'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HTRANKING'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATRANKING'] . "</td>";
  print "<td class='tdClassSold' align='center'>" . number_format($miza,0) . "</td>";
  print "<td class='tdClassSold' align='center'>" . number_format($castig,0) . "</td>";
  print "<td class='tdClassSold' align='center'>" . number_format($sold,0) . "</td>";
  print "<td class='" . $class . "' align='center'>" . number_format($miza_zilnica,0) . "</td>";
  print "<td class='" . $class . "' align='center'>" . number_format($castig_zilnic,0) . "</td>";
  print "<td class='" . $class . "' align='center'>" . number_format($sold_zilnic,0) . "</td>";

  if($current_day==date('D', strtotime($row['dataj'])))
  {
    $suma_zilnica+=$castig;
    //print "<td class='" . $class . "' align='center'>&nbsp;</td>";
  }

  else 
  {
    //print "<td class='" . $class . "' align='center'>".number_format($suma_zilnica,0)."</td>";
    $suma_zilnica=0;
    $miza_zilnica=$sold_zilnic/8;
    $current_day=date('D', strtotime($row['dataj']));
  }
  $i++;
  print "</tr>";
}

print "</table>";
mysqli_close($conn);
?>

</body>
</html>