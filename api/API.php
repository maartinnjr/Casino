<?php
date_default_timezone_set('America/Santiago');

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

// Conexión con la base de datos
$servidor = "127.0.0.1";
$usuario = "root";
$contrasena = "";
$base_de_datos = "casinodb";
$puerto = 3306;

$conexion = new mysqli($servidor, $usuario, $contrasena, $base_de_datos, $puerto);

if ($conexion->connect_error) {
    die(json_encode(["error" => "Conexión fallida: " . $conexion->connect_error]));
}

// --- CONSULTA SQL CORREGIDA ---
// Ahora se ordena por el 'id' de la partida para asegurar que sean las últimas.
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

$resultado = $conexion->query($sql);

$datos_combinados = [];
if ($resultado && $resultado->num_rows > 0) {
    while($fila = $resultado->fetch_assoc()) {
        $fecha = new DateTime($fila['fecha']);
        $fila['fecha_formateada'] = $fecha->format('d/m H:i');
        $datos_combinados[] = $fila;
    }
}

$conexion->close();

echo json_encode($datos_combinados);
?>