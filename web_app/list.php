<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">
  <link rel="stylesheet"  type="text/css" href="css/myclass.css?v=1.2">

</head>
<?php 

//include "config.php";
print "<h1 align='center'>Lista ligilor/tarilor din dataset </h1>";

$servername = "my_bet_db";
$username = "sda";
$password = "sda";
$dbname = "soccer_analysis"; 
$conn = new mysqli($servername, $username, $password, $dbname);

if($conn->connect_error) {
    die("Connection Failed" . $conn->connect_error);
}


function  NumarMeciuriSezon($conn,$sezon1, $divizia,$country)
{
    $NrInreg=0;
    $query = "select count(*) as NrInreg from  games where sezon1=".$sezon1." and divizia='".$divizia."' and country='".$country."'";
    $result = mysqli_query($conn, $query);
    
    //print $query;
    $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
          // print $row["divizia"];
        $NrInreg=$row["NrInreg"];
    return $NrInreg;
}

$divizia =array();
$country=array();
$query = "select distinct  divizia, country  from games order by country asc";
$result = mysqli_query($conn, $query);

$nr_ligi=0;
while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) 
{
    // print $row["divizia"];
    $divizia[$nr_ligi]=$row['divizia'];
    $country[$nr_ligi]=$row['country'];
     $nr_ligi++;        
}


print "<table style='margin: 0px auto;align='center'>";
print "<tr> <td class='celulaTabel'></td><td class='celulaTabel'></td><td class='celulaTabel'></td>";
for ($j=2025;$j>2012;$j--)
    print "<td class='celulaTabel'>".$j."</td>";
print "</tr>";

for($i=0;$i<$nr_ligi;$i++)
{
    print ("<td  class='celulaTabel'>".($i+1)."</td>");
    print ("<td  class='celulaTabel'>".$country[$i]."</td>");
    print ("<td  class='celulaTabel'>".$divizia[$i]."</td>");
    for ($j=2025;$j>2012;$j--)
    {
        $query = "select count(*) as NrInreg from games where country='".$country[$i]."' and divizia='".$divizia[$i]."' and sezon1 =".$j;
        $result = mysqli_query($conn, $query);
        $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
      
        
        
        print ("<td  class='celulaTabel'><a class='legatura' href='meciuri_liga.php?sezon1=".$j."&divizia=".$divizia[$i]."&country=".$country[$i]."'>".$row['NrInreg']."</a></td>");

    }
    print "</tr>";
}
print ("</table>");
$result->free();
?>
