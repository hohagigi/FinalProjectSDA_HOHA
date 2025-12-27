<?php 


$servername = "localhost";
$username = "root";
$password = "depechemode";
$dbname = "soccer_analysis"; 
$conn = new mysqli($servername, $username, $password, $dbname);

if($conn->connect_error) {

    die("Connection Failed" . $conn->connect_error);

}

function  NumarMeciuriSezon($conn,$sezon1)
{
    $NrInreg=0;
    $query = "select max(id) as MaxId from  stats_games where sezon1=".$sezon1." and sold_final>0";
    $MaxId=0;
    $result = mysqli_query($conn, $query);
    
    if(mysqli_num_rows($result)==0) return 0;
    $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
    $MaxId=$row["MaxId"];
    if(is_null($MaxId)) return 0;
    $SoldFinal=0;   
    
    $query = "select sold_final from  stats_games where id=".$MaxId;
    $result = mysqli_query($conn, $query);
    if(mysqli_num_rows($result)>0)
        {
        $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
        $SoldFinal=$row["sold_final"];   
        }
    return $SoldFinal;
}

$tabel= array();
$query = "select distinct sezon1  from stats_games order by sezon1 desc";
$result = mysqli_query($conn, $query);
while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
      // print $row["divizia"];
    $tabel[$row["sezon1"]]=1;
  }


print "<table>";
print "<tr>";
for ($j=2025;$j>2005;$j--)
    print "<td>".$j."</td>";
print "</tr>";
print "<tr>";
for ($j=2025;$j>2005;$j--)
    // print "<td align='right'>".number_format(NumarMeciuriSezon($conn,$j,$divizia[$x]),0)."</td>";
    print "<td align='right'><a href='detalii4.php?sezon=".$j."'>".number_format(NumarMeciuriSezon($conn,$j,),0)."</a></td>";

print "</tr>";
print "</table>";



/* free result set */
$result->free();



?>
