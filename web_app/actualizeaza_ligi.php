<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" href="css/myclass.css">
</head>
<style>

</style>
<?php
echo "<h1 style='text-align:center'>Actualizarea bazei de date cu ligile</h1><br>";
//ob_flush();
flush(); 
$servername = "my_bet_db";
$username = "sda";
$password = "sda";
$dbname = "soccer_analysis";
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) 
  {
  die("Connection Failed" . $conn->connect_error);
}

$result = file_get_contents("https://api.football-data-api.com/league-list?key=54eafef24f9884e1f5ba5a23ced7a8a74cf858378172bee8abc4698cf8e6d73a");
$result = json_decode($result, true);
$nr_ligi_actualizate=0;
$nr_total_ligi=0;
$leagues = $result['data'];
foreach($leagues as $league)
  {
  // echo $league['league_name']." ";
  // echo $league['country']." ";
   foreach ( $league['season'] as $x )
    {
    $nr_total_ligi ++;
    //echo $x['id']." ".$x['year']." ";

    //i9n cazul in care anul e scris pe 8 caractere yyyyzzzz
    if (strlen ( $x['year']) == 8) 
      {
        $year1= substr($x['year'],0,4);
        $year2= substr($x['year'],4,4);  
      } 

    if (strlen ( $x['year']) == 4) 
      {
        $year1= $x['year'];
        $year2= $year1;  
      }  
      
        // verific daca exista liga in baza de date
        $query = "select * from  leagues where  league_id =".$x['id'];
        $result = mysqli_query($conn, $query);
        if(mysqli_num_rows($result)==0) 
        {
          $nr_ligi_actualizate++;    
          // elimin spatiile din numele ligii
          //elimin caracterul apostrof din numele ligii
          $string1 = strtolower(str_replace(' ', '', $league['league_name']));
          $string1 = strtolower(str_replace("'", '', $string1));
          
          $string2 = strtolower(str_replace(' ', '', $league['country']));
          //liga nu exista si trebuie introdusa
          $query1 = "INSERT INTO `soccer_analysis`.`leagues` (`league_id`, `league_name`, `sezon1`, `sezon2`, `country`)
          values ('".$x['id']."','".$string1."','".(int)$year1."','".(int)$year2."','".$string2."')";
          ##print $query1;
          $result1 = mysqli_query($conn, $query1);
          //
          echo "Adaugare liga: <strong>" .htmlspecialchars($string2)." ".htmlspecialchars($string1) . "</strong><br>";
          //ob_flush();
          flush(); 
      }     
    }

  //echo "<br>";
  }
print ("<h3>In footystats.org sunt ".$nr_total_ligi."</h3>");
print ("<h3>In dataset au fost adaugate ".$nr_ligi_actualizate."</h3>");


// if (isset($_GET['sezon'])) $sezon=$_GET['sezon'];
// else $sezon=2024;

// if (isset($_GET['divizia'])) $divizia=$_GET['divizia'];
// else $divizia=0;

$result->free();

// $sql = "INSERT INTO current stock (ItemNumber, Stock) VALUES (?, ?)";

// if (!($stmt = mysqli_prepare($con, $sql))) {
//     die('Error: ' . mysqli_error($con));
// }

// if (!mysqli_stmt_bind_param($stmt, "ii", $_POST[ItemNumber], $_POST[Stock])) {
//     die('Error: ' . mysqli_stmt_error($stmt));
// }

// if (!mysqli_stmt_execute($stmt)) {
//     die('Error: ' . mysqli_stmt_error($stmt));
// }

?>

</body>

</html>


