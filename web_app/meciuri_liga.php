<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" href="css/myclass.css?v=1.2">
</head>
<style>

</style>
<h1 align='center'>Lista meciurilor urmatoare</h1>
<?php


$servername = "my_bet_db";
$username = "sda";
$password = "sda";
$dbname = "soccer_analysis";
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {

  die("Connection Failed" . $conn->connect_error);

}

if (isset($_GET['sezon1'])) $sezon=$_GET['sezon1'];
else $sezon=0;

if (isset($_GET['divizia'])) $divizia=$_GET['divizia'];
else $divizia="";

if (isset($_GET['country'])) $country=$_GET['country'];
else $country="";

$query = "select * from  games where  divizia='".$divizia."' and sezon1=".$sezon." and country='".$country."' order by dataj desc";
$i=0;
$result = mysqli_query($conn, $query);
//if(mysqli_num_rows($result)==0) return 0;
  $class = "randTabelList";
print "<table border=0 align='center' cellspacing=1 cellpadding=1>";
print "<tr class='aTabletr'>";
print "<td class='" . $class . "' align-'center'>" . $i . "</td>";
print "<td class='" . $class . "'>Tara</td>";
print "<td class='" . $class . "'>Liga</td>";
print "<td class='" . $class . "' align='center'>Data</td>";
print "<td class='" . $class . "'>Gazde</td>";
print "<td class='" . $class . "'>Oaspeti</td>";
print "<td class='" . $class . "'>Status</td>";
print "<td class='" . $class . "'>FTHG</td>";
print "<td class='" . $class . "'>FTAG</td>";

print "<td class='" . $class . "'>1</td>";
print "<td class='" . $class . "'>x</td>";
print "<td class='" . $class . "'>2</td>";
print "<td class='" . $class . "'>Etapa</td>";
print "<td class='" . $class . "'>GMHT1</td>";
print "<td class='" . $class . "'>GMHT!</td>";
print "<td class='" . $class . "'>GPHT1</td>";
print "<td class='" . $class . "'>GPHT1</td>";

print "<td class='" . $class . "'>GMAT1</td>";
print "<td class='" . $class . "'>GMAT1</td>";
print "<td class='" . $class . "'>GPAT1</td>";
print "<td class='" . $class . "'>GPAT1</td>";

print "<td class='" . $class . "'>Loc H</td>";
print "<td class='" . $class . "'>Loc A</td>";

print "<td class='" . $class . "'>P H</td>";
print "<td class='" . $class . "'>P A</td>";
print "<td class='" . $class . "'>Coef H H</td>";
print "<td class='" . $class . "'>Coef H A</td>";

print "<td class='" . $class . "'>Coef A H</td>";
print "<td class='" . $class . "'>Coef A A</td>";

print "</tr>";
$i = 1;
while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {

  $class = "randTabelList";

  print "<tr class='aTabletr'>";
  print "<td class='" . $class . "'>" . $i . "</td>";
  print "<td class='" . $class . "'>" . $row['country'] . "</td>";
  print "<td class='" . $class . "'>" . $row['divizia'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['dataj'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HomeTeam'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['AwayTeam'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['status'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['FTHG'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['FTAG'] . "</td>";
  
  print "<td class='" . $class . "' align='center'>" . $row['B365H'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['B365D'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['B365A'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['MatchDay'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HTGM1'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HTGM2'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HTGP1'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HTGP2'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATGM1'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATGM2'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATGP1'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATGP2'] . "</td>";
  
  print "<td class='" . $class . "' align='center'>" . $row['HTRANKING'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATRANKING'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HTPOINTS'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATPOINTS'] . "</td>";
  
  print "<td class='" . $class . "' align='center'>" . $row['HTCOEF1'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['HTCOEF2'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATCOEF1'] . "</td>";
  print "<td class='" . $class . "' align='center'>" . $row['ATCOEF2'] . "</td>";
  $i++;

  print "</tr>";
}
print "</table>";

$result->free();



?>

</body>

</html>