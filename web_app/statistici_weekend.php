<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" href="css/mycss.css">
</head>
<style>

</style>
<h1 align='center'>Precizia predictiilor </h1>
<h4 align="center">(pe fiecare liga in parte/pe fiecare tip de rezultat/ over all )</h4>

<?php
$servername = "127.0.0.1";
$username = "root";
$password = "depechemode";
$dbname = "soccer_analysis";
$conn = mysqli_connect($servername, $username, $password, $dbname);

if ($conn->connect_error) 
  {
    print "Eroare la coneciune";
  die("Connection Failed" . $conn->connect_error);
}

$query = "select  * from  games where  status='complete' 
        and ((dataj>'2021-08-02' and dataj<'2022-04-21')
        or (dataj>'2022-08-02' and dataj<'2023-04-21') 
        or (dataj>'2023-08-02' and dataj<'2024-04-21')  
        or (dataj>'2024-08-02' and dataj<'2025-04-21')  
        or (dataj>'2025-08-02' and dataj<'2026-04-21')) order by dataj asc";
$result = mysqli_query($conn, $query);
print "<table style='margin: 0px auto;align='center'>";
print "<tr  class='aTabletr'>";
print "<td class='" . $class . "'>Nr crt</td>";
print "<td class='" . $class . "' align='center'>Data</td>";
print "<td class='" . $class . "'>Nr corecte</td>";
print "<td class='" . $class . "'>Nr gresite</td>";
print "<td class='" . $class . "' align='center'>Procent</td>";
print "<td class='" . $class . "'>Nr corecte</td>";
print "<td class='" . $class . "'>Nr gresite</td>";
print "<td class='" . $class . "' align='center'>Procent</td>";
print "<td class='" . $class . "'>Nr corecte</td>";
print "<td class='" . $class . "'>Nr gresite</td>";
print "<td class='" . $class . "' align='center'>Procent</td>";
print "<td class='" . $class . "'>Nr corecte</td>";
print "<td class='" . $class . "'>Nr gresite</td>";
print "<td class='" . $class . "' align='center'>Procent</td>";

print "</tr>";
$i = 1;

$current_date = '2021-08-01';
$correct_predictions1 = 0;
$wrong_predictions1 = 0;
$correct_predictions2 = 0;
$wrong_predictions2 = 0;
$correct_predictions3 = 0;
$wrong_predictions3 = 0;
$correct_predictions4 = 0;
$wrong_predictions4 = 0;

while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) 
{
    if($current_date != substr($row['dataj'],0,10))
    {
        print "<tr>";
        print "<td class='" . $class . "' align='center'>" . $i . "</td>";
        print "<td class='" . $class . "' align='center'>" . $current_date . "</td>";
        print "<td class='" . $class . "' align='center'>" . $correct_predictions1 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $wrong_predictions1 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $correct_predictions1-$wrong_predictions1 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $correct_predictions2 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $wrong_predictions2 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $correct_predictions2-$wrong_predictions2 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $correct_predictions3 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $wrong_predictions3 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $correct_predictions3-$wrong_predictions3 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $correct_predictions4 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $wrong_predictions4 . "</td>";
        print "<td class='" . $class . "' align='center'>" . $correct_predictions4-$wrong_predictions4 . "</td>";
        print "</tr>";
        $current_date=substr($row['dataj'],0,10);
        $correct_predictions1=0;
        $wrong_predictions1=0;
        $correct_predictions2=0;
        $wrong_predictions2=0;
        $correct_predictions3=0;
        $wrong_predictions3=0;
        $correct_predictions4=0;
        $wrong_predictions4=0;
        $i++;
    }

    if ($current_date == substr($row['dataj'],0,10))
    {
        if ($row['pred1']==2 and $row['FTR']==2)
            $correct_predictions1++;
        if ($row['pred1']==2 and $row['FTR']!=2)
            $wrong_predictions1++;

        if ($row['pred2']==2 and $row['FTR']==2)
            $correct_predictions2++;
        if ($row['pred2']==2 and $row['FTR']!=2)
            $wrong_predictions2++;

        if ($row['predDT']==2 and $row['FTR']==2)
            $correct_predictions3++;
        if ($row['predDT']==2 and $row['FTR']!=2)
            $wrong_predictions3++;

        if ($row['predXGB']==2 and $row['FTR']==2)
            $correct_predictions4++;
        if ($row['predXGB']==2 and $row['FTR']!=2)
            $wrong_predictions4++;
    }

}
print "<tr>";
print "<td class='" . $class . "' align='center'>" . $i . "</td>";
print "<td class='" . $class . "' align='center'>" . $current_date . "</td>";
print "<td class='" . $class . "' align='center'>" . $correct_predictions1 . "</td>";
print "<td class='" . $class . "' align='center'>" . $wrong_predictions1 . "</td>";
print "<td class='" . $class . "' align='center'>" . $correct_predictions1-$wrong_predictions1 . "</td>";
print "<td class='" . $class . "' align='center'>" . $correct_predictions2 . "</td>";
print "<td class='" . $class . "' align='center'>" . $wrong_predictions2 . "</td>";
print "<td class='" . $class . "' align='center'>" . $correct_predictions2-$wrong_predictions2 . "</td>";
print "<td class='" . $class . "' align='center'>" . $correct_predictions3 . "</td>";
print "<td class='" . $class . "' align='center'>" . $wrong_predictions3 . "</td>";
print "<td class='" . $class . "' align='center'>" . $correct_predictions3-$wrong_predictions3 . "</td>";
print "<td class='" . $class . "' align='center'>" . $correct_predictions3 . "</td>";
print "<td class='" . $class . "' align='center'>" . $wrong_predictions4 . "</td>";
print "<td class='" . $class . "' align='center'>" . $correct_predictions4-$wrong_predictions4 . "</td>";
print "</tr>";



print "</table>";
mysqli_close($conn);
?>

</body>
</html>