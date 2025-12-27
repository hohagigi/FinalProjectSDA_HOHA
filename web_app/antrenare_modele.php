<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Antrenare modelul AI</title>
</head>
<body>
    <h1 align='center'>Antrenare modele AI </h1>


    
    <h2 align='center'>Matricea de confuzie</h2>
    <table align='center'>
        <tr>    
            <td align='center'><button onclick="runTrainingCB()">Rulează antrenarea CB</button></td>
            <td align='center'><button onclick="runTrainingDT()">Rulează antrenarea DT</button></td>
            <td align='center'><button onclick="runTrainingNN()">Rulează antrenarea NN</td>

        </tr>
        <tr>
            <td align='center'> <div id="cb-container"></div></td>
            <td align='center'> <div id="dt-container"></div></td>
            <td align='center'> <div id="nn-container"></div></td>

        </tr>
    </table>
   

    <script>
        async function runTrainingCB() {
            const container = document.getElementById("cb-container");
            container.innerHTML = "Se rulează modelul...";

            try {
                const response = await fetch("http://127.0.0.1:8000/train/CB");
                const data = await response.json();

                const cm = data.confusion_matrix; // listă de liste

                // Construim un mic tabel HTML
                let html = "<table border='1' cellpadding='5'>";
                for (let i = 0; i < cm.length; i++) {
                    html += "<tr>";
                    for (let j = 0; j < cm[i].length; j++) {
                        html += "<td>" + cm[i][j] + "</td>";
                    }
                    html += "</tr>";
                }
                html += "</table>";
                container.innerHTML = html;
            } catch (err) {
                container.innerHTML = "Eroare: " + err;
            }
        }
    </script>




<script>
        async function runTrainingDT() {
            const container = document.getElementById("dt-container");
            container.innerHTML = "Se rulează modelul...";

            try {
                const response = await fetch("http://127.0.0.1:8000/train/DT");
                const data = await response.json();

                const cm = data.confusion_matrix; // listă de liste

                // Construim un mic tabel HTML
                let html = "<table border='1' cellpadding='5'>";
                for (let i = 0; i < cm.length; i++) {
                    html += "<tr>";
                    for (let j = 0; j < cm[i].length; j++) {
                        html += "<td>" + cm[i][j] + "</td>";
                    }
                    html += "</tr>";
                }
                html += "</table>";
                container.innerHTML = html;
            } catch (err) {
                container.innerHTML = "Eroare: " + err;
            }
        }
    </script>

<script>
        async function runTrainingNN() {
            const container = document.getElementById("nn-container");
            container.innerHTML = "Se rulează modelul...";

            try {
                const response = await fetch("http://127.0.0.1:8000/train/NN");
                const data = await response.json();

                const cm = data.confusion_matrix; // listă de liste

                // Construim un mic tabel HTML
                let html = "<table border='1' cellpadding='5'>";
                for (let i = 0; i < cm.length; i++) {
                    html += "<tr>";
                    for (let j = 0; j < cm[i].length; j++) {
                        html += "<td>" + cm[i][j] + "</td>";
                    }
                    html += "</tr>";
                }
                html += "</table>";
                container.innerHTML = html;
            } catch (err) {
                container.innerHTML = "Eroare: " + err;
            }
        }
</script>    
</body>
</html>