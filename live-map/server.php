<?php

include("config.php");

$show_errors = false;
if ($show_errors) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $DATA_URL);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    "Authorization: Basic $BASIC_TOKEN",
    "Content-Type: application/json"
));
$response = curl_exec($ch);
print_r($response);
curl_close($ch); 

?>
