<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Actualizare clasamente</title>
</head>
<body>
    <h1 align='center'>Actualizare clasamente si coeficientii Pi rating </h1>


    <table align='center'>
        <tr>    
            <td align='center'><button onclick="runUpdateClasamente()">Rulează actualizare clasamente</button></td>
            <td align='center'><button onclick="runUpdatePiRating()">Rulează actualizare PI Rating</button></td>

        </tr>
        <tr>
            <td align='center'> <div id="container1"></div></td>
            <td align='center'> <div id="container2"></div></td>


        </tr>
    </table>
   

    <script>
        async function runUpdateClasamente() {
            const container = document.getElementById("container1");
            container.innerHTML = "Se actualizeaza clasamente...";

            try {
                const response = await fetch("http://localhost:8000/update/UpdateClasamente");
                const data = await response.json();

                const nrp = data.numar_inreg; 

                // Construim un mic tabel HTML
                let html = "<table border='1' cellpadding='5'>";
                    html += "<tr>";
                    html += "<td>" + nrp + "</td>";
                    html += "</tr>";
                    html += "</table>";
                container.innerHTML = html;
            } catch (err) {
                container.innerHTML = "Eroare: " + err;
            }
        }
    </script>

<script>
        async function runUpdatePiRating() {
            const container = document.getElementById("container2");
            container.innerHTML = "Se actualizeaza clasamente...";

            try {
                const response = await fetch("http://localhost:8000/update/UpdatePiRating");
                const data = await response.json();

                const nrp = data.numar_inreg; 

                // Construim un mic tabel HTML
                let html = "<table border='1' cellpadding='5'>";
                    html += "<tr>";
                    html += "<td>" + nrp + "</td>";
                    html += "</tr>";
                    html += "</table>";
                container.innerHTML = html;
            } catch (err) {
                container.innerHTML = "Eroare: " + err;
            }
        }
    </script>



</body>
</html>