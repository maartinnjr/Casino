<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

// Conexión con la base de datos
$servidor = "127.0.0.1";
$usuario = "Casino";
$contrasena = "casino123";
$base_de_datos = "casinodb";
$puerto = 3306;

$conexion = new mysqli($servidor, $usuario, $contrasena, $base_de_datos, $puerto);

if ($conexion->connect_error) {
    die(json_encode(["error" => "Conexión fallida: " . $conexion->connect_error]));
}

// Consulta SQL actualizada para obtener el TOP 10
$sql = "
    SELECT 
        u.usuario, 
        u.tipo_moneda,
        h.id_juego, 
        h.apuesta
    FROM 
        usuarios u
    INNER JOIN 
        historial_partidas h ON u.id_usuario = h.id_usuario
    ORDER BY
        h.apuesta DESC
    LIMIT 10
";

$resultado = $conexion->query($sql);

$datos_combinados = [];
if ($resultado && $resultado->num_rows > 0) {
    while($fila = $resultado->fetch_assoc()) {
        $datos_combinados[] = $fila;
    }
}

$conexion->close();

echo json_encode($datos_combinados);
?>