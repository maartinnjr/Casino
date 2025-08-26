<?php
date_default_timezone_set('America/Santiago');

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

$servidor = "127.0.0.1";
$usuario = "root";
$contrasena = "";
$base_de_datos = "casinodb";
$puerto = 3306;

$conexion = new mysqli($servidor, $usuario, $contrasena, $base_de_datos, $puerto);

if ($conexion->connect_error) {
    die(json_encode(["error" => "Conexión fallida: " . $conexion->connect_error]));
}

$accion = isset($_GET['accion']) ? $_GET['accion'] : 'historial';

if ($accion == 'ranking_usuarios') {
    // --- CONSULTA PARA EL RANKING DE USUARIOS (AHORA LIMIT 10) ---
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
    $resultado = $conexion->query($sql);
    $datos = [];
    if ($resultado && $resultado->num_rows > 0) {
        while($fila = $resultado->fetch_assoc()) {
            $datos[] = $fila;
        }
    }
    echo json_encode($datos);

} else {
    // --- CONSULTA PARA EL HISTORIAL DE PARTIDAS (POR DEFECTO) ---
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
    $datos = [];
    if ($resultado && $resultado->num_rows > 0) {
        while($fila = $resultado->fetch_assoc()) {
            $datos[] = $fila;
        }
    }
    echo json_encode($datos);
}

$conexion->close();
?>