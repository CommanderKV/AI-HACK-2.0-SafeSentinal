<?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $links = $_POST["links"];
        $command = escapeshellcmd('python ai-analize.py ' . $links);
        $output = shell_exec($command);
        echo $output;
        echo $_POST["links"];
    }
?>