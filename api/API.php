<?php
date_default_timezone_set('America/Santiago');

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

$servidor = "127.0.0.1";
$usuario = "Casino";
$contrasena = "casino123";
$base_de_datos = "casinodb";
$puerto = 3306;

$conexion = new mysqli($servidor, $usuario, $contrasena, $base_de_datos, $puerto);

if ($conexion->connect_error) {
    die(json_encode(["error" => "Conexión fallida: " . $conexion->connect_error]));
}

$accion = isset($_GET['accion']) ? $_GET['accion'] : 'historial';
$sql = '';

if ($accion == 'ranking_usuarios') {
    $sql = "
        SELECT 
            usuario, 
            saldo
        FROM 
            usuarios
        ORDER BY
            saldo DESC
        LIMIT 10
    ";
} elseif ($accion == 'historial') {
    $sql = "
        SELECT 
            u.usuario, 
            h.apuesta,
            h.resultado,
            h.fecha,
            j.nombre_juego
        FROM 
            usuarios u
        INNER JOIN 
            historial_partidas h ON u.id_usuario = h.id_usuario
        INNER JOIN
            juegos j ON h.id_juego = j.id_juego
        ORDER BY
            h.id DESC
        LIMIT 10
    ";
}

$datos = [];
if (!empty($sql)) {
    $resultado = $conexion->query($sql);
    if ($resultado && $resultado->num_rows > 0) {
        while($fila = $resultado->fetch_assoc()) {
            $datos[] = $fila;
        }
    }
}

echo json_encode($datos);

$conexion->close();
?>