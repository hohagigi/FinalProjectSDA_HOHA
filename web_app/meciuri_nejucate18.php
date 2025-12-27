<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" href="css/mycss.css?v=1.2">
</head>
<style>
</style>

<?php
$servername = "localhost";
$username = "ai";
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
else $castigator=-1;

if(isset($_GET["sortare_dupa_liga"])) $sortare_dupa_liga=$_GET["sortare_dupa_liga"];
else $sortare_dupa_liga=2;

if(isset($_GET["sortare_dupa_data"])) $sortare_dupa_data=$_GET["sortare_dupa_data"];
else $sortare_dupa_data=0;

if(isset($_GET["liga"]))  $liga=$_GET["liga"];
else $liga="toate";

if(isset($_GET["tip_pred"]))  $tip_pred=$_GET["tip_pred"];
else $tip_pred="predDT";

?>

<h1 align='center'>Lista meciurilor urmatoare</h1>
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
                    <input type="radio" id="id_egalitate" name="castigator" value="1" <?php if ($castigator==1) print ("checked")  ?> >
                    <label for="id_egalitate">egalitate</label>
                  </td>
                </tr>
              </table>         
          </td>

          <td>
              <table>
                <tr>
                  <td class='tdClassSelect' style="text-align:left;">
                    <input type="radio" id="id_oaspeti" name="castigator" value="2" <?php if ($castigator==2) print ("checked")  ?> >
                    <label for="id_oaspeti">oaspeti</label>
                  </td>
                </tr>
                <tr>
                  <td class='tdClassSelect' style="text-align:left;">
                    <input type="radio" id="id_toate" name="castigator" value="-1" <?php if ($castigator==-1) print ("checked")  ?>>
                    <label for="id_toate">toate</label>
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
                      if ($tip_pred=="pred1") print ("<option value='pred1' selected>Pred (liga)</option><br>");
                        else                          print ("<option value='pred1' >Pred (liga)</option><br>");
                     
                      if ($tip_pred=="pred2") print ("<option value='pred2' selected>Pred (all)</option><br>");
                        else                          print ("<option value='pred2' >Pred (all)</option><br>");
                      
                      if ($tip_pred=="predDT")  print ("<option value='predDT' selected>Pred DT</option><br>");
                        else                            print ("<option value='predDT' >Pred DT</option><br>");
                     
                      if ($tip_pred=="predXGB") print ("<option value='predXGB' selected>Pred CatBoosts</option><br>");
                        else                            print ("<option value='predXGB' >Pred CatBoosts</option><br>");
                      
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
$query="select * from games where status='incomplete' and atranking-htranking>7 and 
      dataj>='".$data_inceput."' and dataj <='".$data_sfarsit." 23:59' ";
if ($castigator>=0 && $castigator<=2)
    $query=$query." and ".$tip_pred."=".$castigator;

if($liga!="toate")
  $query=$query." and divizia='".$liga."' ";

if($sortare_dupa_data!=2 || $sortare_dupa_liga!=2)
$query=$query." order by ";

if ($sortare_dupa_liga==0)
    $query=$query." divizia asc";
if ($sortare_dupa_liga==1)
    $query=$query." divizia desc";

if (($sortare_dupa_liga==0 || $sortare_dupa_liga==1) && ($sortare_dupa_data==0 || $sortare_dupa_data==1))
  $query=$query." , ";

if ($sortare_dupa_data==0)
    $query=$query." dataj asc";
if ($sortare_dupa_data==1)
    $query=$query." dataj desc";


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
print "<td class='" . $class . "'>Pred 1 NN<br>(league)</td>";
// print "<td class='" . $class . "'>Pred 1<br>(league)</td>";
// print "<td class='" . $class . "'>Pred X<br>(league)</td>";
// print "<td class='" . $class . "'>Pred 2<br>(league)</td>";
print "<td class='" . $class . "'>Pred 2 NN<br>(all)</td>";
// print "<td class='" . $class . "'>Pred 1<br>(all)</td>";
// print "<td class='" . $class . "'>Pred X<br>(all)</td>";
// print "<td class='" . $class . "'>Pred 2<br>(all)</td>";
print "<td class='" . $class . "'>Pred DT<br>(all)</td>";
print "<td class='" . $class . "'>Pred CB<br>(all)</td>";


print "</tr>";
$i = 1;
while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
  $class = "tdClass";
  print "<tr class='trClass'>";
  print "<td class='" . $class . "' >" . $i . "</td>";
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
  print "<td  class='" . $class . "' align='center'>" . $row['LastGamesHome'] . "</td>";
  print "<td  class='" . $class . "' align='center'>" . $row['LastGamesAway'] . "</td>";

  if($row['pred1']==0)
    {
    print "<td class='tdClass0'>" . $row['pred1'] . "</td>";
    // print "<td class='tdClass0'>" . $row['pred1_1'] . "</td>";
    // print "<td class='tdClass0'>" . $row['pred1_x'] . "</td>";
    // print "<td class='tdClass0' align='center'>" . $row['pred1_2'] . "</td>";
    }

 if($row['pred1']==1)
    {
    print "<td class='tdClass1'>" . $row['pred1'] . "</td>";
    // print "<td class='tdClass1'>" . $row['pred1_1'] . "</td>";
    // print "<td class='tdClass1'>" . $row['pred1_x'] . "</td>";
    // print "<td class='tdClass1' align='center'>" . $row['pred1_2'] . "</td>";
    }

  if($row['pred1']==2)
    {
    print "<td class='tdClass2'>" . $row['pred1'] . "</td>";
    // print "<td class='tdClass2'>" . $row['pred1_1'] . "</td>";
    // print "<td class='tdClass2'>" . $row['pred1_x'] . "</td>";
    // print "<td class='tdClass2' align='center'>" . $row['pred1_2'] . "</td>";
    }

  if($row['pred2']==0)
    {
    print "<td class='tdClass0'>" . $row['pred2'] . "</td>";
    // print "<td class='tdClass0'>" . $row['pred2_1'] . "</td>";
    // print "<td class='tdClass0'>" . $row['pred2_x'] . "</td>";
    // print "<td class='tdClass0' align='center'>" . $row['pred2_2'] . "</td>";
    }

 if($row['pred2']==1)
    {
    print "<td class='tdClass1'>" . $row['pred2'] . "</td>";
    // print "<td class='tdClass1'>" . $row['pred2_1'] . "</td>";
    // print "<td class='tdClass1'>" . $row['pred2_x'] . "</td>";
    // print "<td class='tdClass1' align='center'>" . $row['pred2_2'] . "</td>";
    }

  if($row['pred2']==2)
    {
    print "<td class='tdClass2'>" . $row['pred2'] . "</td>";
    // print "<td class='tdClass2'>" . $row['pred2_1'] . "</td>";
    // print "<td class='tdClass2'>" . $row['pred2_x'] . "</td>";
    // print "<td class='tdClass2' align='center'>" . $row['pred2_2'] . "</td>";
    }      

  $name_of_class = "tdClass".$row['predDT'];
  print "<td class='".$name_of_class."'>" . $row['predDT'] . "</td>";
    
  $name_of_class = "tdClass".$row['predXGB'];
  print "<td class='".$name_of_class."'>" . $row['predXGB'] . "</td>";
  
  $i++;
  print "</tr>";
}
print "</table>";
?>

</body>
</html>