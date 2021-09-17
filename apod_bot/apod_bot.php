<?php

// Variables
//// Identificador del chat de Telegram

$chat_id = "chat_id"; // poner el adecuado
//// Identificador del bot
$bot_id     = "bot_id"; // poner el adecuado
//// API NASA Token
$api_nasa_token = "api_nasa_token"; // poner el adecuado

// Obtenemos imagen del APOD del día y la guardamos en el servidor
$imagen_apod_url = json_decode(file_get_contents("https://api.nasa.gov/planetary/apod?&api_key=".$api_nasa_token), TRUE)["url"];
$fecha_apod = json_decode(file_get_contents("https://api.nasa.gov/planetary/apod?&api_key=".$api_nasa_token), TRUE)["date"];
$url_destino_imagen = "/images/apod_".$fecha_apod.".jpg";
//file_put_contents($url_destino_imagen, file_get_contents($imagen_apod_url);
$ch1 = curl_init($imagen_apod_url);
$fp = fopen(__DIR__.$url_destino_imagen, 'wb');
curl_setopt($ch1, CURLOPT_FILE, $fp);
curl_setopt($ch1, CURLOPT_HEADER, 0);
curl_exec($ch1);
curl_close($ch1);
fclose($fp);

// Obtenemos la descripción de la imagen
$apod_explanation = json_decode(file_get_contents("https://api.nasa.gov/planetary/apod?&api_key=".$api_nasa_token), TRUE)["explanation"];
//$apod_title = json_decode(file_get_contents("https://api.nasa.gov/planetary/apod?&api_key=".$api_nasa_token), TRUE)["title"];

// Enviamos el título de la imagen
//$apod_title_message = "La imagen de hoy es: ".$apod_title
//file_get_contents($bot_url."sendmessage?chat_id=".$chat_id."&text=".rawurlencode($apod_title));

// Enviamos imagen al chat de Telegram
$bot_url    = "https://api.telegram.org/bot".$bot_id."/";
$url_send_photo  = $bot_url . "sendPhoto?chat_id=" . $chat_id ;

$post_fields = array('chat_id'   => $chat_id,
    'photo'     => new CURLFile(realpath(__DIR__.$url_destino_imagen))
);

$ch = curl_init(); 
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    "Content-Type:multipart/form-data"
));
curl_setopt($ch, CURLOPT_URL, $url_send_photo); 
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
curl_setopt($ch, CURLOPT_POSTFIELDS, $post_fields); 
$output = curl_exec($ch);

// Enviamos la descripción

file_get_contents($bot_url."sendmessage?chat_id=".$chat_id."&text=".rawurlencode($apod_explanation));
?>
