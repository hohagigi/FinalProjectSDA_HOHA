<?php 


$servername = "localhost";
$username = "root";
$password = "depechemode";
$dbname = "soccer_analysis"; 
$conn = new mysqli($servername, $username, $password, $dbname);

if($conn->connect_error) {

    die("Connection Failed" . $conn->connect_error);

}

function  NumarMeciuriSezon($conn,$sezon1, $divizia)
{
    $NrInreg=0;
    $query = "select max(id) as MaxId from  stats_games where sezon1=".$sezon1." and divizia='".$divizia."' and sold_final>0";
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
$query = "select distinct sezon1 , divizia from stats_games group by divizia,sezon1  order by sezon1 desc";
$result = mysqli_query($conn, $query);
while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
      // print $row["divizia"];
    $tabel[$row["sezon1"]][$row["divizia"]]=1;
  }
$divizia =array();
$query = "select distinct  divizia from stats_games order by divizia desc";
$result = mysqli_query($conn, $query);
$i=0;
while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) 
{
    // print $row["divizia"];
    $divizia[$i]=$row['divizia'];
     $i++;        
}
print "<table>";
print "<tr><td></td>";
for ($j=2025;$j>2005;$j--)
    print "<td>".$j."</td>";
print "</tr>";
for ($x=0;$x<$i;$x++)
{
     print "<tr>";
     print "<td>".$divizia[$x]."</td>";
        for ($j=2025;$j>2005;$j--)
        {
            if (array_key_exists($j,$tabel))
                if($tabel[$j][$divizia[$x]]==1) 
                {   
                    // print "<td align='right'>".number_format(NumarMeciuriSezon($conn,$j,$divizia[$x]),0)."</td>";
                    print "<td align='right'><a href='detalii1.php?sezon=".$j."&divizia=".$divizia[$x]."'>".number_format(NumarMeciuriSezon($conn,$j,$divizia[$x]),0)."</a></td>";
                }
                else 
                {
                    print $tabel[$j][$divizia[$x]];
                }
            else print "<td>0</td>";
        }
     print "</tr>";
}
print "</table>";


/* free result set */
$result->free();



?>
