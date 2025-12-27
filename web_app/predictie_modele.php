<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Predictie meciuri</title>
</head>
<body>
    <h1 align='center'>Predictie meciuri ce urmeaza a se disputa </h1>


    
    <h2 align='center'>Tipuri de algoritmi AI</h2>
    <table align='center'>
        <tr>    
            <td align='center'><button onclick="runPredictCB()">Rulează CatBoost</button></td>
            <td align='center'><button onclick="runPredictDT()">Rulează Decision Tree</button></td>
            <td align='center'><button onclick="runPredictNN()">Rulează Neuronal Network</td>

        </tr>
        <tr>
            <td align='center'> <div id="cb-container"></div></td>
            <td align='center'> <div id="dt-container"></div></td>
            <td align='center'> <div id="nn-container"></div></td>

        </tr>
    </table>
   

    <script>
        async function runPredictCB() {
            const container = document.getElementById("cb-container");
            container.innerHTML = "Se rulează modelul...";

            try {
                const response = await fetch("http://127.0.0.1:8000/predict/CB");
                const data = await response.json();

                const nrp = data.numar_predictii; 

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
        async function runPredictDT() {
            const container = document.getElementById("dt-container");
            container.innerHTML = "Se rulează modelul...";

            try {
                const response = await fetch("http://127.0.0.1:8000/predict/DT");
                const data = await response.json();

                const nrp = data.numar_predictii;

                // Construim un mic tabel HTML
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
        async function runPredictNN() {
            const container = document.getElementById("nn-container");
            container.innerHTML = "Se rulează modelul...";

            try {
                const response = await fetch("http://127.0.0.1:8000/predict/NN");
                const data = await response.json();

                const nrp = data.numar_predictii;

                // Construim un mic tabel HTML
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