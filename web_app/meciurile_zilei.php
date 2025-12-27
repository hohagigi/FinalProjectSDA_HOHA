<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" href="css/mycss.css">
</head>
<style>

</style>
<h1 align='center'>Meciurile zilei</h1>

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

$today = date("Y-m-d");
$tomorow = date("Y-m-d",strtotime("tomorrow"));

$query = "select * from  games where  status='incomplete' and dataj>='".$today."' and dataj<'".$tomorow."' 
            and pred2=2 order by dataj asc";

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

  
  $i++;
  print "</tr>";
}
print "</table>";
?>

</body>
</html>