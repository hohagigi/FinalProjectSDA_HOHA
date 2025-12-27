<?php 


$servername = "localhost";
$username = "ai";
$password = "sda";
$dbname = "games"; 
$conn = new mysqli($servername, $username, $password, $dbname);

if($conn->connect_error) {

    die("Connection Failed" . $conn->connect_error);

}

if (isset($_GET['sezon'])) $sezon=$_GET['sezon'];
else $sezon=0;

if (isset($_GET['divizia'])) $divizia=$_GET['divizia'];
else $divizia=0;


$query = "select * from  games where sezon1=".$sezon." and divizia='".$divizia."' and (PlaceAway-PlaceHome>8)";

$result = mysqli_query($conn, $query);
//if(mysqli_num_rows($result)==0) return 0;
   
print "<table border=1>";

while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) 
{

    if($row['castigat']==1 && $row['sold_initial']>0) print "<tr bgcolor='#00aaaa'>";
    if($row['castigat']==0 && $row['sold_initial']>0) print "<tr bgcolor='#aa0000'>";
    if($row['sold_initial==0']) print "<tr bgcolor='#ffffff'>";
    
    print "<td>".$row['HomeTeam']."</td>";
    print "<td>".$row['AwayTeam']."</td>";
    print "<td>".$row['FTHG']."</td>";
    print "<td>".$row['FTAG']."</td>";
    print "<td>".$row['B365H']."</td>";
    print "<td>".$row['B365D']."</td>";
    print "<td>".$row['B365A']."</td>";
    print "<td>".$row['sold_initial']."</td>";
    print "<td>".$row['cota']."</td>";
    print "<td>".$row['castigat']."</td>";
    print "<td>".$row['sold_final']."</td>";
    
     
    
    print "</tr>";
  }
print "</table>";

$result->free();



?>
