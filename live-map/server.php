<?php

include("config.php");

$show_errors = false;
if ($show_errors) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://geo-tracker-live.herokuapp.com/location-data?limit=100');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    "Authorization: Basic $BASIC_TOKEN"
));
$response = curl_exec($ch);
$result = json_decode($response);
print_r($result);
curl_close($ch); 

?>
