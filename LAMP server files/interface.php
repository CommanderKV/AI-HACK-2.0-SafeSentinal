<?php
    header("Content-Type: text/plain");
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $links = $_POST["links"];
        $output = shell_exec("python ai-analize.py $links");
        echo $output;
        echo $_POST["links"];
    }
?>