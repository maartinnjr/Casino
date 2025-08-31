-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-08-2025 a las 21:31:56
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `casinodb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administradores`
--

CREATE TABLE `administradores` (
  `id_admin` int(11) NOT NULL,
  `usuario` varchar(255) NOT NULL,
  `contrasena` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administradores`
--

INSERT INTO `administradores` (`id_admin`, `usuario`, `contrasena`) VALUES
(1, 'admincasino', 'adminpalacio');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bancos`
--

CREATE TABLE `bancos` (
  `id_banco` int(11) NOT NULL,
  `nombre_banco` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `bancos`
--

INSERT INTO `bancos` (`id_banco`, `nombre_banco`) VALUES
(1, 'Banco de Chile'),
(2, 'Banco Santander'),
(3, 'BancoEstado'),
(4, 'Scotiabank'),
(5, 'Banco de Crédito e Inversiones (BCI)');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `canjes_dulces`
--

CREATE TABLE `canjes_dulces` (
  `id_canje` int(11) NOT NULL,
  `id_admin` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `dulces_canjeados` int(11) NOT NULL,
  `costo_saldo` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `canjes_dulces`
--

INSERT INTO `canjes_dulces` (`id_canje`, `id_admin`, `id_usuario`, `dulces_canjeados`, `costo_saldo`, `fecha`) VALUES
(1, 1, 3, 6, 30000, '2025-08-11 01:28:23'),
(2, 1, 1, 6, 30000, '2025-08-20 14:37:44');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comunas`
--

CREATE TABLE `comunas` (
  `id_comuna` int(11) NOT NULL,
  `nombre_comuna` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comunas`
--

INSERT INTO `comunas` (`id_comuna`, `nombre_comuna`) VALUES
(1, 'Cerrillos'),
(2, 'Cerro Navia'),
(3, 'Conchalí'),
(4, 'El Bosque'),
(5, 'Estación Central'),
(6, 'Huechuraba'),
(7, 'Independencia'),
(8, 'La Cisterna'),
(9, 'La Florida'),
(10, 'La Granja'),
(11, 'La Pintana'),
(12, 'La Reina'),
(13, 'Las Condes'),
(14, 'Lo Barnechea'),
(15, 'Lo Espejo'),
(16, 'Lo Prado'),
(17, 'Macul'),
(18, 'Maipú'),
(19, 'Ñuñoa'),
(20, 'Pedro Aguirre Cerda'),
(21, 'Peñalolén'),
(22, 'Providencia'),
(23, 'Pudahuel'),
(24, 'Quilicura'),
(25, 'Quinta Normal'),
(26, 'Recoleta'),
(27, 'Renca'),
(28, 'San Joaquín'),
(29, 'San Miguel'),
(30, 'San Ramón'),
(31, 'Santiago'),
(32, 'Vitacura'),
(33, 'Puente Alto'),
(34, 'Pirque'),
(35, 'San José de Maipo'),
(36, 'Colina'),
(37, 'Lampa'),
(38, 'Tiltil'),
(39, 'San Bernardo'),
(40, 'Buin'),
(41, 'Calera de Tango'),
(42, 'Paine'),
(43, 'Melipilla'),
(44, 'Alhué'),
(45, 'Curacaví'),
(46, 'María Pinto'),
(47, 'San Pedro'),
(48, 'Talagante'),
(49, 'El Monte'),
(50, 'Isla de Maipo'),
(51, 'Padre Hurtado'),
(52, 'Peñaflor');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_partidas`
--

CREATE TABLE `historial_partidas` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_juego` int(11) NOT NULL,
  `apuesta` int(11) NOT NULL,
  `resultado` varchar(50) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historial_partidas`
--

INSERT INTO `historial_partidas` (`id`, `id_usuario`, `id_juego`, `apuesta`, `resultado`, `fecha`) VALUES
(1, 1, 1, 1000, 'empate', '2025-08-08 10:05:36'),
(2, 1, 1, 1000, 'empate', '2025-08-08 10:10:38'),
(3, 1, 1, 1000, 'empate', '2025-08-08 10:39:47'),
(4, 1, 1, 1000, 'empate', '2025-08-08 10:43:29'),
(5, 1, 1, 1000, 'ganaste', '2025-08-08 10:46:16'),
(6, 1, 1, 1000, 'empate', '2025-08-08 10:49:22'),
(7, 4, 2, 500, 'ganaste', '2025-08-08 10:54:40'),
(8, 4, 3, 500, 'perdiste', '2025-08-08 10:55:13'),
(9, 4, 2, 1000, 'ganaste', '2025-08-08 10:55:42'),
(10, 4, 1, 500, 'perdiste', '2025-08-08 10:58:00'),
(11, 4, 3, 1000, 'perdiste', '2025-08-08 11:00:43'),
(12, 4, 3, 1000, 'perdiste', '2025-08-08 11:01:04'),
(13, 4, 2, 1000, 'perdiste', '2025-08-08 11:01:22'),
(14, 4, 2, 1000, 'perdiste', '2025-08-08 11:01:38'),
(15, 5, 1, 1000, 'ganaste', '2025-08-08 11:09:50'),
(16, 5, 2, 100000, 'perdiste', '2025-08-08 11:11:10'),
(17, 1, 1, 1000, 'perdiste', '2025-08-08 11:14:19'),
(18, 1, 1, 1000, 'ganaste', '2025-08-10 23:15:40'),
(19, 1, 1, 1000, 'empate', '2025-08-10 23:16:37'),
(20, 1, 2, 1000, 'perdiste', '2025-08-10 23:22:27'),
(21, 1, 2, 1000, 'perdiste', '2025-08-10 23:24:52'),
(22, 1, 2, 200, 'ganaste', '2025-08-10 23:28:53'),
(23, 1, 2, 500, 'perdiste', '2025-08-10 23:29:19'),
(24, 1, 2, 500, 'perdiste', '2025-08-10 23:29:50'),
(25, 1, 2, 100, 'ganaste', '2025-08-10 23:30:05'),
(26, 1, 1, 200, 'empate', '2025-08-10 23:35:08'),
(27, 1, 1, 200, 'empate', '2025-08-10 23:35:18'),
(28, 1, 1, 100, 'ganaste', '2025-08-10 23:36:05'),
(29, 1, 1, 200, 'ganaste', '2025-08-10 23:37:24'),
(30, 1, 1, 500, 'perdiste', '2025-08-10 23:37:52'),
(31, 1, 1, 10, 'ganaste', '2025-08-10 23:38:58'),
(32, 1, 3, 10, 'empate', '2025-08-10 23:39:54'),
(33, 1, 1, 10, 'ganaste', '2025-08-10 23:41:19'),
(34, 1, 1, 100, 'ganaste', '2025-08-10 23:44:01'),
(35, 1, 3, 100, 'empate', '2025-08-10 23:48:57'),
(36, 1, 2, 1000, 'ganaste', '2025-08-10 23:52:06'),
(37, 1, 3, 200, 'perdiste', '2025-08-10 23:53:10'),
(38, 1, 2, 1000, 'ganaste', '2025-08-11 00:01:12'),
(39, 1, 3, 1000, 'perdiste', '2025-08-11 00:01:35'),
(40, 1, 3, 1000, 'perdiste', '2025-08-11 00:08:59'),
(41, 1, 3, 1000, 'ganaste', '2025-08-11 00:18:02'),
(42, 1, 3, 1000, 'empate', '2025-08-11 00:21:31'),
(43, 1, 3, 200, 'perdiste', '2025-08-11 00:24:45'),
(44, 1, 3, 1000, 'perdiste', '2025-08-11 00:29:15'),
(46, 1, 4, 1000, 'ganaste', '2025-08-11 01:03:02'),
(47, 1, 4, 1000, 'ganaste', '2025-08-11 01:08:46'),
(48, 1, 1, 1000, 'perdiste', '2025-08-11 01:28:41'),
(49, 1, 2, 1000, 'ganaste', '2025-08-11 01:28:57'),
(50, 1, 3, 1000, 'perdiste', '2025-08-11 01:29:17'),
(51, 1, 4, 1000, 'perdiste', '2025-08-11 01:29:32'),
(52, 1, 1, 1000, 'perdiste', '2025-08-11 01:31:13'),
(53, 1, 1, 1000, 'empate', '2025-08-11 01:31:41'),
(54, 1, 1, 1000, 'ganaste', '2025-08-11 01:32:39'),
(55, 1, 2, 1000, 'ganaste', '2025-08-11 01:33:03'),
(56, 1, 3, 1000, 'ganaste', '2025-08-11 01:33:29'),
(57, 1, 4, 1000, 'ganaste', '2025-08-11 01:33:51'),
(58, 6, 1, 1000, 'ganaste', '2025-08-11 12:20:28'),
(59, 6, 2, 1000, 'perdiste', '2025-08-11 12:20:52'),
(60, 6, 3, 1000, 'empate', '2025-08-11 12:21:15'),
(61, 6, 4, 1000, 'ganaste', '2025-08-11 12:21:32'),
(62, 7, 1, 200, 'ganaste', '2025-08-11 12:25:23'),
(63, 7, 2, 500, 'perdiste', '2025-08-11 12:26:12'),
(64, 7, 3, 500, 'perdiste', '2025-08-11 12:26:53'),
(65, 7, 4, 1000, 'ganaste', '2025-08-11 12:27:25'),
(66, 1, 4, 1000, 'ganaste', '2025-08-11 15:01:52'),
(67, 1, 4, 1000, 'ganaste', '2025-08-11 15:02:28'),
(68, 1, 4, 1000, 'perdiste', '2025-08-11 15:08:16'),
(69, 1, 4, 1000, 'ganaste', '2025-08-13 09:01:33'),
(70, 1, 4, 1000, 'ganaste', '2025-08-13 09:01:49'),
(71, 1, 4, 1000, 'perdiste', '2025-08-13 09:02:12'),
(72, 1, 4, 1000, 'ganaste', '2025-08-13 09:04:49'),
(73, 1, 4, 1000, 'ganaste', '2025-08-13 09:05:03'),
(74, 1, 4, 1000, 'ganaste', '2025-08-13 09:05:19'),
(75, 1, 4, 1000, 'ganaste', '2025-08-13 09:08:27'),
(76, 1, 3, 1000, 'perdiste', '2025-08-13 09:08:49'),
(77, 1, 4, 1000, 'ganaste', '2025-08-13 09:09:25'),
(78, 1, 4, 1000, 'perdiste', '2025-08-13 09:09:54'),
(79, 1, 2, 1000, 'perdiste', '2025-08-13 09:11:08'),
(80, 1, 4, 1000, 'ganaste', '2025-08-13 09:11:35'),
(81, 1, 4, 1000, 'perdiste', '2025-08-13 09:21:47'),
(82, 1, 4, 1000, 'ganaste', '2025-08-14 10:17:20'),
(83, 8, 3, 500, 'empate', '2025-08-18 19:19:04'),
(84, 8, 4, 1000, 'ganaste', '2025-08-18 19:19:29'),
(85, 8, 1, 500, 'ganaste', '2025-08-18 19:19:57'),
(86, 8, 4, 1000, 'ganaste', '2025-08-18 19:20:57'),
(87, 8, 1, 1000, 'empate', '2025-08-18 19:21:27'),
(88, 8, 2, 200, 'ganaste', '2025-08-18 19:21:40'),
(89, 8, 1, 1000, 'perdiste', '2025-08-18 19:21:54'),
(90, 8, 1, 1000, 'perdiste', '2025-08-18 19:22:07'),
(91, 8, 2, 500, 'ganaste', '2025-08-18 19:22:23'),
(92, 8, 1, 1000, 'ganaste', '2025-08-18 19:22:37'),
(93, 8, 1, 2000, 'ganaste', '2025-08-18 19:22:55'),
(94, 8, 1, 3000, 'empate', '2025-08-18 19:23:29'),
(95, 8, 1, 3000, 'perdiste', '2025-08-18 19:23:46'),
(96, 8, 1, 1000, 'perdiste', '2025-08-18 19:24:12'),
(97, 8, 2, 500, 'perdiste', '2025-08-18 19:24:25'),
(98, 8, 1, 1000, 'perdiste', '2025-08-18 19:25:30'),
(99, 8, 2, 200, 'perdiste', '2025-08-18 19:25:48'),
(100, 8, 2, 200, 'perdiste', '2025-08-18 19:26:02'),
(101, 8, 2, 100, 'perdiste', '2025-08-18 19:26:16'),
(102, 8, 2, 100, 'ganaste', '2025-08-18 19:26:27'),
(103, 8, 2, 100, 'perdiste', '2025-08-18 19:26:40'),
(104, 8, 2, 200, 'perdiste', '2025-08-18 19:26:52'),
(105, 1, 4, 25000, 'perdiste', '2025-08-19 16:05:05'),
(106, 1, 3, 1000, 'perdiste', '2025-08-19 16:06:26'),
(107, 1, 1, 1000, 'perdiste', '2025-08-19 16:06:35'),
(108, 1, 1, 1000, 'ganaste', '2025-08-19 16:06:44'),
(109, 1, 2, 60000, 'perdiste', '2025-08-19 16:24:09'),
(110, 1, 2, 9000, 'ganaste', '2025-08-20 12:34:30'),
(111, 1, 1, 1000, 'perdiste', '2025-08-20 12:47:22'),
(112, 1, 1, 1000, 'empate', '2025-08-20 12:47:53'),
(113, 1, 1, 17000, 'ganaste', '2025-08-20 12:48:08'),
(114, 1, 3, 1000, 'ganaste', '2025-08-20 12:48:27'),
(115, 1, 1, 35000, 'empate', '2025-08-20 12:48:52'),
(116, 1, 1, 35000, 'perdiste', '2025-08-20 12:49:06'),
(117, 1, 1, 1000, 'empate', '2025-08-20 12:50:09'),
(118, 1, 1, 20000, 'perdiste', '2025-08-20 12:50:26'),
(119, 1, 1, 49000, 'perdiste', '2025-08-20 12:51:09'),
(120, 1, 1, 1000, 'perdiste', '2025-08-20 14:35:35'),
(121, 1, 1, 1000, 'perdiste', '2025-08-20 14:35:48'),
(122, 1, 2, 1000, 'ganaste', '2025-08-20 14:36:03'),
(123, 1, 3, 1000, 'perdiste', '2025-08-20 14:36:20'),
(124, 1, 1, 1000, 'empate', '2025-08-20 14:38:18'),
(125, 1, 4, 1000, 'ganaste', '2025-08-21 14:08:42'),
(126, 1, 4, 1000, 'ganaste', '2025-08-21 14:23:42'),
(127, 1, 4, 1000, 'perdiste', '2025-08-21 14:24:02'),
(128, 1, 4, 1000, 'ganaste', '2025-08-21 14:27:35'),
(129, 1, 4, 1000, 'ganaste', '2025-08-21 14:32:20'),
(130, 1, 4, 1000, 'perdiste', '2025-08-21 14:35:06'),
(131, 1, 4, 1000, 'ganaste', '2025-08-21 14:35:22'),
(132, 1, 4, 1000, 'perdiste', '2025-08-21 14:36:11'),
(133, 1, 4, 1000, 'ganaste', '2025-08-21 14:41:44'),
(134, 1, 4, 1000, 'perdiste', '2025-08-21 14:42:01'),
(135, 1, 4, 1000, 'perdiste', '2025-08-21 14:47:23'),
(136, 1, 3, 1000, 'perdiste', '2025-08-21 14:47:30'),
(137, 1, 4, 1000, 'perdiste', '2025-08-21 14:47:43'),
(138, 1, 4, 1000, 'ganaste', '2025-08-21 14:48:03'),
(139, 1, 4, 1000, 'ganaste', '2025-08-21 14:48:14'),
(140, 1, 3, 1000, 'perdiste', '2025-08-21 14:48:22'),
(141, 1, 4, 1000, 'perdiste', '2025-08-21 14:48:32'),
(142, 1, 4, 1000, 'perdiste', '2025-08-21 14:48:50'),
(143, 1, 4, 1000, 'ganaste', '2025-08-21 14:49:07'),
(144, 1, 1, 1000, 'perdiste', '2025-08-25 12:41:26'),
(145, 1, 4, 1000, 'ganaste', '2025-08-25 12:42:06'),
(146, 1, 4, 1000, 'ganaste', '2025-08-25 12:51:08'),
(147, 1, 1, 1000, 'empate', '2025-08-25 12:52:10'),
(148, 1, 1, 1000, 'perdiste', '2025-08-25 12:52:24'),
(149, 1, 1, 1000, 'empate', '2025-08-25 12:58:03'),
(150, 1, 1, 1000, 'empate', '2025-08-25 13:03:56'),
(151, 1, 1, 1000, 'empate', '2025-08-25 13:09:46'),
(152, 1, 4, 1000, 'empate', '2025-08-25 13:15:55'),
(153, 1, 4, 1000, 'ganaste', '2025-08-25 13:16:01'),
(154, 1, 1, 1000, 'ganaste', '2025-08-25 13:26:44'),
(155, 4, 1, 500, 'empate', '2025-08-25 14:09:57'),
(156, 4, 1, 500, 'empate', '2025-08-25 14:09:59'),
(157, 4, 1, 500, 'ganaste', '2025-08-25 14:10:12'),
(158, 4, 2, 500, 'perdiste', '2025-08-25 14:10:54'),
(159, 4, 1, 1000, 'perdiste', '2025-08-25 14:11:12'),
(160, 1, 4, 1000, 'perdiste', '2025-08-25 14:23:48'),
(161, 1, 2, 1000, 'ganaste', '2025-08-25 14:24:57'),
(162, 1, 2, 1000, 'perdiste', '2025-08-25 14:25:08'),
(163, 1, 1, 1000, 'empate', '2025-08-25 14:25:47'),
(164, 1, 1, 1000, 'empate', '2025-08-25 14:25:54'),
(165, 1, 4, 1000, 'empate', '2025-08-25 14:26:20'),
(166, 1, 4, 1000, 'empate', '2025-08-25 14:26:33'),
(168, 1, 4, 12000, 'perdiste', '2025-08-25 14:37:20'),
(169, 1, 4, 50000, 'ganaste', '2025-08-25 14:38:06'),
(170, 1, 2, 1000, 'ganaste', '2025-08-25 14:38:23'),
(171, 1, 4, 1000, 'ganaste', '2025-08-25 14:45:59'),
(172, 1, 4, 1000, 'perdiste', '2025-08-25 14:46:08'),
(173, 1, 4, 1000, 'perdiste', '2025-08-25 14:46:20'),
(174, 10, 1, 2000, 'perdiste', '2025-08-25 15:09:40'),
(175, 10, 1, 500, 'empate', '2025-08-25 15:09:43'),
(176, 10, 2, 5000, 'perdiste', '2025-08-25 15:10:44'),
(177, 10, 2, 5000, 'perdiste', '2025-08-25 15:10:58'),
(178, 10, 2, 1000, 'empate', '2025-08-25 15:11:00'),
(179, 10, 1, 10000, 'ganaste', '2025-08-25 15:11:21'),
(180, 10, 1, 20000, 'ganaste', '2025-08-25 15:11:36'),
(181, 10, 1, 500, 'empate', '2025-08-25 15:11:38'),
(182, 1, 1, 1000, 'ganaste', '2025-08-25 16:24:53'),
(183, 1, 1, 1000, 'ganaste', '2025-08-25 16:53:35'),
(184, 1, 1, 500, 'empate', '2025-08-25 16:53:37'),
(185, 12, 3, 1000, 'perdiste', '2025-08-25 18:16:51'),
(186, 12, 1, 1000, 'ganaste', '2025-08-25 18:17:52'),
(187, 12, 1, 500, 'perdiste', '2025-08-25 18:18:22'),
(188, 4, 2, 100, 'ganaste', '2025-08-25 18:18:54'),
(189, 12, 1, 500, 'ganaste', '2025-08-25 18:18:57'),
(190, 12, 1, 500, 'ganaste', '2025-08-25 18:19:04'),
(191, 4, 2, 500, 'perdiste', '2025-08-25 18:19:13'),
(192, 12, 1, 1000, 'ganaste', '2025-08-25 18:19:26'),
(193, 12, 1, 500, 'perdiste', '2025-08-25 18:19:35'),
(194, 4, 2, 1000, 'empate', '2025-08-25 18:19:41'),
(195, 4, 2, 1000, 'empate', '2025-08-25 18:19:43'),
(196, 4, 2, 500, 'empate', '2025-08-25 18:19:44'),
(197, 4, 2, 200, 'empate', '2025-08-25 18:19:46'),
(198, 4, 2, 200, 'empate', '2025-08-25 18:19:47'),
(199, 4, 2, 1000, 'empate', '2025-08-25 18:19:48'),
(200, 4, 2, 200, 'empate', '2025-08-25 18:19:49'),
(201, 4, 2, 200, 'empate', '2025-08-25 18:19:50'),
(202, 12, 1, 1000, 'ganaste', '2025-08-25 18:19:53'),
(203, 4, 2, 200, 'empate', '2025-08-25 18:19:51'),
(204, 4, 2, 1000, 'empate', '2025-08-25 18:19:52'),
(205, 4, 2, 200, 'empate', '2025-08-25 18:19:53'),
(206, 4, 2, 200, 'empate', '2025-08-25 18:19:53'),
(207, 4, 2, 200, 'empate', '2025-08-25 18:19:54'),
(208, 12, 1, 1000, 'ganaste', '2025-08-25 18:20:16'),
(209, 4, 2, 1000, 'ganaste', '2025-08-25 18:20:14'),
(210, 1, 2, 1000, 'perdiste', '2025-08-25 18:20:18'),
(211, 1, 2, 1000, 'empate', '2025-08-25 18:20:20'),
(212, 12, 1, 1000, 'empate', '2025-08-25 18:20:59'),
(213, 4, 2, 1000, 'perdiste', '2025-08-25 18:21:01'),
(214, 12, 1, 1000, 'ganaste', '2025-08-25 18:21:08'),
(215, 4, 2, 1000, 'empate', '2025-08-25 18:21:06'),
(216, 4, 2, 1000, 'perdiste', '2025-08-25 18:21:27'),
(217, 12, 1, 1000, 'perdiste', '2025-08-25 18:21:30'),
(218, 1, 2, 1000, 'perdiste', '2025-08-25 18:21:29'),
(219, 1, 2, 1000, 'empate', '2025-08-25 18:21:31'),
(220, 4, 2, 1000, 'ganaste', '2025-08-25 18:21:38'),
(221, 12, 1, 1000, 'ganaste', '2025-08-25 18:21:41'),
(222, 12, 1, 1000, 'ganaste', '2025-08-25 18:21:51'),
(223, 4, 2, 1000, 'perdiste', '2025-08-25 18:21:49'),
(224, 4, 2, 500, 'perdiste', '2025-08-25 18:21:57'),
(225, 12, 1, 1000, 'perdiste', '2025-08-25 18:21:59'),
(226, 1, 1, 1000, 'perdiste', '2025-08-25 18:22:01'),
(227, 12, 1, 1000, 'perdiste', '2025-08-25 18:22:07'),
(228, 12, 1, 1000, 'ganaste', '2025-08-25 18:22:14'),
(229, 4, 2, 600, 'ganaste', '2025-08-25 18:22:18'),
(230, 12, 1, 1000, 'ganaste', '2025-08-25 18:22:27'),
(231, 4, 2, 1000, 'ganaste', '2025-08-25 18:22:28'),
(232, 12, 1, 1000, 'empate', '2025-08-25 18:22:36'),
(233, 12, 1, 1000, 'ganaste', '2025-08-25 18:22:45'),
(234, 4, 2, 1200, 'perdiste', '2025-08-25 18:22:48'),
(235, 12, 1, 1000, 'ganaste', '2025-08-25 18:22:59'),
(236, 4, 2, 500, 'ganaste', '2025-08-25 18:22:59'),
(237, 13, 1, 1000, 'ganaste', '2025-08-25 18:21:48'),
(238, 12, 1, 1000, 'ganaste', '2025-08-25 18:23:09'),
(239, 13, 1, 500, 'empate', '2025-08-25 18:21:51'),
(240, 4, 2, 500, 'ganaste', '2025-08-25 18:23:09'),
(241, 4, 2, 1000, 'perdiste', '2025-08-25 18:23:18'),
(242, 13, 2, 1000, 'ganaste', '2025-08-25 18:22:12'),
(243, 12, 1, 1000, 'ganaste', '2025-08-25 18:23:31'),
(244, 12, 1, 1000, 'perdiste', '2025-08-25 18:23:42'),
(245, 13, 2, 1000, 'perdiste', '2025-08-25 18:22:24'),
(246, 12, 1, 1000, 'ganaste', '2025-08-25 18:23:50'),
(247, 4, 1, 500, 'perdiste', '2025-08-25 18:23:50'),
(248, 13, 4, 1000, 'ganaste', '2025-08-25 18:22:40'),
(249, 4, 1, 500, 'perdiste', '2025-08-25 18:23:58'),
(250, 4, 1, 500, 'ganaste', '2025-08-25 18:24:05'),
(251, 13, 4, 1000, 'ganaste', '2025-08-25 18:22:49'),
(252, 4, 1, 500, 'ganaste', '2025-08-25 18:24:14'),
(253, 12, 1, 1000, 'perdiste', '2025-08-25 18:24:23'),
(254, 4, 1, 500, 'perdiste', '2025-08-25 18:24:21'),
(255, 4, 1, 500, 'empate', '2025-08-25 18:24:41'),
(256, 4, 1, 1000, 'empate', '2025-08-25 18:24:42'),
(257, 4, 1, 1000, 'empate', '2025-08-25 18:24:43'),
(258, 4, 1, 500, 'empate', '2025-08-25 18:24:43'),
(259, 4, 1, 500, 'empate', '2025-08-25 18:24:45'),
(260, 12, 1, 1000, 'ganaste', '2025-08-25 18:24:50'),
(261, 4, 1, 1000, 'ganaste', '2025-08-25 18:24:55'),
(262, 12, 1, 1000, 'ganaste', '2025-08-25 18:25:00'),
(263, 13, 2, 1000, 'perdiste', '2025-08-25 18:23:47'),
(264, 4, 1, 500, 'perdiste', '2025-08-25 18:25:09'),
(265, 4, 1, 1000, 'perdiste', '2025-08-25 18:25:16'),
(266, 12, 1, 1000, 'ganaste', '2025-08-25 18:25:19'),
(267, 4, 1, 500, 'ganaste', '2025-08-25 18:25:25'),
(268, 13, 3, 500, 'perdiste', '2025-08-25 18:24:11'),
(269, 12, 1, 1000, 'ganaste', '2025-08-25 18:25:33'),
(270, 4, 1, 500, 'ganaste', '2025-08-25 18:25:31'),
(271, 4, 1, 500, 'ganaste', '2025-08-25 18:25:37'),
(272, 4, 1, 1000, 'ganaste', '2025-08-25 18:25:46'),
(273, 13, 3, 1000, 'perdiste', '2025-08-25 18:24:30'),
(274, 12, 1, 1000, 'perdiste', '2025-08-25 18:25:57'),
(275, 4, 1, 1000, 'empate', '2025-08-25 18:25:57'),
(276, 13, 1, 500, 'ganaste', '2025-08-25 18:24:46'),
(277, 13, 1, 1000, 'perdiste', '2025-08-25 18:24:50'),
(278, 13, 1, 500, 'perdiste', '2025-08-25 18:24:58'),
(279, 13, 1, 500, 'perdiste', '2025-08-25 18:25:04'),
(280, 4, 1, 3500, 'perdiste', '2025-08-25 18:26:21'),
(281, 13, 1, 500, 'perdiste', '2025-08-25 18:25:09'),
(282, 13, 1, 500, 'empate', '2025-08-25 18:25:17'),
(283, 13, 1, 500, 'perdiste', '2025-08-25 18:25:26'),
(284, 13, 1, 500, 'ganaste', '2025-08-25 18:25:30'),
(285, 13, 1, 500, 'perdiste', '2025-08-25 18:25:41'),
(286, 4, 3, 1000, 'empate', '2025-08-25 18:28:03'),
(287, 12, 1, 5000, 'perdiste', '2025-08-25 18:28:09'),
(288, 1, 2, 1000, 'perdiste', '2025-08-25 18:28:07'),
(289, 1, 2, 1000, 'ganaste', '2025-08-25 18:28:15'),
(290, 1, 2, 1000, 'perdiste', '2025-08-25 18:28:24'),
(291, 4, 1, 10000, 'empate', '2025-08-25 18:28:27'),
(292, 1, 2, 1000, 'perdiste', '2025-08-25 18:28:42'),
(293, 1, 2, 1000, 'perdiste', '2025-08-25 18:28:50'),
(294, 4, 1, 10000, 'perdiste', '2025-08-25 18:28:51'),
(295, 4, 1, 1000, 'ganaste', '2025-08-25 18:29:01'),
(296, 12, 1, 5000, 'perdiste', '2025-08-25 18:29:04'),
(297, 4, 1, 1000, 'empate', '2025-08-25 18:29:06'),
(298, 4, 1, 11000, 'perdiste', '2025-08-25 18:29:25'),
(299, 4, 1, 500, 'perdiste', '2025-08-25 18:29:32'),
(300, 12, 1, 10000, 'empate', '2025-08-25 18:29:35'),
(301, 1, 4, 23778, 'perdiste', '2025-08-25 18:28:23'),
(302, 4, 1, 60000, 'ganaste', '2025-08-25 18:29:54'),
(303, 12, 1, 10000, 'ganaste', '2025-08-25 18:30:01'),
(304, 1, 2, 22222, 'ganaste', '2025-08-25 18:29:00'),
(305, 1, 2, 1000, 'empate', '2025-08-25 18:29:02'),
(306, 4, 1, 9000, 'ganaste', '2025-08-25 18:30:37'),
(307, 12, 1, 30000, 'ganaste', '2025-08-25 18:30:39'),
(308, 1, 1, 94444, 'perdiste', '2025-08-25 18:29:24'),
(309, 12, 1, 60000, 'ganaste', '2025-08-25 18:31:10'),
(310, 4, 1, 38000, 'perdiste', '2025-08-25 18:31:09'),
(311, 1, 4, 90000, 'perdiste', '2025-08-25 18:30:05'),
(312, 1, 4, 500, 'empate', '2025-08-25 18:30:07'),
(313, 4, 1, 20000, 'empate', '2025-08-25 18:31:26'),
(314, 4, 1, 20000, 'ganaste', '2025-08-25 18:31:48'),
(315, 4, 1, 1000, 'perdiste', '2025-08-25 18:32:05'),
(316, 4, 1, 20000, 'perdiste', '2025-08-25 18:32:17'),
(317, 1, 4, 90000, 'perdiste', '2025-08-25 18:31:09'),
(318, 12, 1, 120000, 'ganaste', '2025-08-25 18:32:31'),
(319, 4, 1, 20000, 'perdiste', '2025-08-25 18:32:49'),
(320, 4, 1, 20000, 'perdiste', '2025-08-25 18:33:06'),
(321, 12, 1, 240000, 'perdiste', '2025-08-25 18:33:21'),
(322, 1, 4, 1000, 'ganaste', '2025-08-25 18:33:27'),
(323, 1, 4, 1000, 'empate', '2025-08-25 18:33:30'),
(324, 4, 1, 59000, 'ganaste', '2025-08-25 18:33:37'),
(325, 4, 1, 59000, 'ganaste', '2025-08-25 18:33:55'),
(326, 12, 1, 5000, 'perdiste', '2025-08-25 18:34:16'),
(327, 4, 1, 59000, 'ganaste', '2025-08-25 18:34:17'),
(328, 4, 1, 59000, 'ganaste', '2025-08-25 18:34:46'),
(329, 14, 1, 500, 'perdiste', '2025-08-25 18:33:35'),
(330, 14, 1, 1000, 'empate', '2025-08-25 18:33:46'),
(331, 4, 1, 59000, 'perdiste', '2025-08-25 18:35:11'),
(332, 4, 1, 59000, 'perdiste', '2025-08-25 18:35:38'),
(333, 4, 1, 100000, 'perdiste', '2025-08-25 18:35:55'),
(334, 4, 1, 59000, 'ganaste', '2025-08-25 18:36:10'),
(335, 14, 1, 1500, 'perdiste', '2025-08-25 18:35:06'),
(336, 4, 1, 59000, 'perdiste', '2025-08-25 18:36:24'),
(337, 12, 1, 5000, 'ganaste', '2025-08-25 18:36:44'),
(338, 4, 1, 1000, 'empate', '2025-08-25 18:36:47'),
(339, 4, 1, 77000, 'ganaste', '2025-08-25 18:37:05'),
(340, 12, 1, 8000, 'perdiste', '2025-08-25 18:37:11'),
(341, 12, 1, 1000, 'perdiste', '2025-08-25 18:37:31'),
(342, 4, 1, 77000, 'perdiste', '2025-08-25 18:37:36'),
(343, 12, 1, 1000, 'perdiste', '2025-08-25 18:37:41'),
(344, 14, 1, 60000, 'ganaste', '2025-08-25 18:36:34'),
(345, 14, 1, 500, 'empate', '2025-08-25 18:36:35'),
(346, 12, 1, 1000, 'perdiste', '2025-08-25 18:38:09'),
(347, 12, 1, 1000, 'ganaste', '2025-08-25 18:41:42'),
(348, 12, 1, 2000, 'perdiste', '2025-08-25 18:42:04'),
(349, 14, 1, 65000, 'perdiste', '2025-08-25 18:41:34'),
(350, 14, 1, 500, 'perdiste', '2025-08-25 18:41:41'),
(351, 14, 2, 100000, 'perdiste', '2025-08-25 18:42:54'),
(352, 12, 1, 5000, 'perdiste', '2025-08-25 18:44:15'),
(353, 14, 2, 1000, 'perdiste', '2025-08-25 18:43:06'),
(354, 12, 1, 1000, 'ganaste', '2025-08-25 18:44:29'),
(355, 14, 2, 150000, 'ganaste', '2025-08-25 18:43:32'),
(356, 12, 1, 4000, 'empate', '2025-08-25 18:44:54'),
(357, 14, 2, 1000, 'empate', '2025-08-25 18:43:37'),
(358, 12, 1, 4000, 'perdiste', '2025-08-25 18:45:47'),
(359, 12, 1, 5000, 'ganaste', '2025-08-25 18:46:37'),
(360, 12, 1, 10000, 'perdiste', '2025-08-25 18:46:56'),
(361, 12, 1, 10000, 'perdiste', '2025-08-25 18:47:22'),
(362, 12, 1, 2000, 'ganaste', '2025-08-25 18:47:50'),
(363, 12, 1, 4000, 'perdiste', '2025-08-25 18:48:13'),
(364, 14, 2, 250000, 'perdiste', '2025-08-25 18:56:37'),
(365, 14, 2, 1000, 'ganaste', '2025-08-25 18:56:50'),
(366, 14, 2, 9000, 'ganaste', '2025-08-25 18:57:26'),
(367, 14, 2, 1000, 'perdiste', '2025-08-25 18:57:36'),
(368, 14, 3, 700, 'empate', '2025-08-25 18:58:19'),
(369, 14, 3, 90000, 'empate', '2025-08-25 18:58:42'),
(370, 14, 3, 90000, 'empate', '2025-08-25 18:59:11'),
(371, 14, 3, 90000, 'empate', '2025-08-25 18:59:34'),
(372, 14, 3, 1000, 'empate', '2025-08-25 18:59:49'),
(373, 14, 3, 1000, 'empate', '2025-08-25 19:00:03'),
(374, 14, 3, 98000, 'empate', '2025-08-25 19:00:24'),
(375, 14, 2, 98000, 'perdiste', '2025-08-25 19:00:50'),
(376, 14, 2, 1000, 'perdiste', '2025-08-25 19:00:58'),
(377, 14, 2, 699000, 'ganaste', '2025-08-25 19:01:27'),
(378, 14, 2, 1000, 'perdiste', '2025-08-25 19:01:43'),
(379, 15, 2, 500, 'ganaste', '2025-08-25 19:03:10'),
(380, 15, 2, 200, 'ganaste', '2025-08-25 19:03:30'),
(381, 15, 3, 1000, 'empate', '2025-08-25 19:05:22'),
(382, 15, 3, 1000, 'empate', '2025-08-25 19:05:50'),
(383, 14, 1, 1000000, 'ganaste', '2025-08-25 19:07:25'),
(384, 15, 3, 1000, 'perdiste', '2025-08-25 19:06:08'),
(385, 15, 2, 500, 'ganaste', '2025-08-25 19:06:30'),
(386, 15, 2, 1000, 'perdiste', '2025-08-25 19:07:20'),
(387, 15, 2, 1000, 'perdiste', '2025-08-25 19:09:40'),
(388, 15, 2, 1000, 'perdiste', '2025-08-25 19:09:49'),
(389, 1, 1, 1000, 'perdiste', '2025-08-25 19:17:15'),
(390, 1, 2, 1000, 'perdiste', '2025-08-25 19:18:08'),
(391, 1, 2, 1000, 'empate', '2025-08-25 19:18:10'),
(392, 1, 4, 1000, 'ganaste', '2025-08-25 19:18:21'),
(393, 16, 1, 1000, 'perdiste', '2025-08-25 19:20:13'),
(394, 16, 1, 1000, 'empate', '2025-08-25 19:21:05'),
(395, 16, 1, 1000, 'perdiste', '2025-08-25 19:21:20'),
(396, 1, 1, 1000, 'ganaste', '2025-08-25 19:24:15'),
(397, 1, 4, 1000, 'ganaste', '2025-08-25 19:24:22'),
(398, 16, 1, 10000, 'perdiste', '2025-08-25 19:24:31'),
(399, 1, 2, 1000, 'ganaste', '2025-08-25 19:24:32'),
(400, 16, 1, 10000, 'empate', '2025-08-25 19:24:55'),
(401, 16, 1, 11000, 'empate', '2025-08-25 19:25:20'),
(402, 16, 1, 11000, 'perdiste', '2025-08-25 19:25:44'),
(403, 16, 1, 11000, 'ganaste', '2025-08-25 19:25:57'),
(404, 16, 1, 1000, 'ganaste', '2025-08-25 19:26:13'),
(405, 10, 1, 20000, 'perdiste', '2025-08-25 19:29:13'),
(406, 10, 1, 20000, 'ganaste', '2025-08-25 19:29:33'),
(407, 17, 2, 1000, 'perdiste', '2025-08-25 19:29:59'),
(408, 17, 3, 1000, 'empate', '2025-08-25 19:30:15'),
(409, 17, 1, 150000, 'ganaste', '2025-08-25 19:30:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos`
--

CREATE TABLE `juegos` (
  `id_juego` int(11) NOT NULL,
  `nombre_juego` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `apuesta_minima` int(11) DEFAULT 100
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `juegos`
--

INSERT INTO `juegos` (`id_juego`, `nombre_juego`, `descripcion`, `apuesta_minima`) VALUES
(1, 'Blackjack', 'El objetivo es sumar 21 puntos o acercarse lo más posible sin pasarse.', 100),
(2, 'Ruleta', 'Apuesta a un color (rojo/negro) y gana si la bola cae en tu elección.', 100),
(3, 'Tragamonedas', 'Elige tu fruta de la suerte y gira los rodillos para ganar.', 100),
(4, 'Coinflip', 'Apuesta a cara o sello y duplica tu monto.', 100);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `transacciones`
--

CREATE TABLE `transacciones` (
  `id_transaccion` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo_transaccion` enum('deposito','retiro','abono') DEFAULT NULL,
  `monto` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `id_banco` int(11) DEFAULT NULL,
  `id_canje` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `transacciones`
--

INSERT INTO `transacciones` (`id_transaccion`, `id_usuario`, `tipo_transaccion`, `monto`, `fecha`, `id_banco`, `id_canje`) VALUES
(1, 1, 'abono', 12, '2025-08-10 23:14:52', NULL, NULL),
(2, 3, 'deposito', 12, '2025-08-10 23:14:52', NULL, NULL),
(3, 1, 'abono', 600, '2025-08-11 01:27:42', NULL, NULL),
(4, 3, 'deposito', 600, '2025-08-11 01:27:42', NULL, NULL),
(5, 3, 'retiro', 30000, '2025-08-11 01:28:23', NULL, 1),
(6, 6, 'abono', 1000, '2025-08-11 12:19:55', NULL, NULL),
(7, 1, 'deposito', 1000, '2025-08-11 12:19:55', NULL, NULL),
(8, 7, 'abono', 100, '2025-08-11 12:24:30', NULL, NULL),
(9, 1, 'deposito', 100, '2025-08-11 12:24:30', NULL, NULL),
(10, 1, 'abono', 9000, '2025-08-11 22:10:11', NULL, NULL),
(11, 6, 'deposito', 9000, '2025-08-11 22:10:11', NULL, NULL),
(12, 1, 'abono', 1000, '2025-08-20 12:50:47', NULL, NULL),
(13, 3, 'deposito', 1000, '2025-08-20 12:50:47', NULL, NULL),
(14, 1, 'retiro', 30000, '2025-08-20 14:37:44', NULL, 2),
(15, 1, 'retiro', 1000, '2025-08-25 14:24:03', NULL, NULL),
(16, 7, 'deposito', 1000, '2025-08-25 14:24:03', NULL, NULL),
(17, 1, 'retiro', 15000, '2025-08-25 14:37:01', NULL, NULL),
(19, 4, 'retiro', 25000, '2025-08-25 18:43:36', NULL, NULL),
(20, 12, 'deposito', 25000, '2025-08-25 18:43:36', NULL, NULL),
(21, 14, 'retiro', 1000000, '2025-08-25 19:22:33', NULL, NULL),
(22, 16, 'deposito', 1000000, '2025-08-25 19:22:33', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `usuario` varchar(255) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `saldo` int(11) NOT NULL,
  `dulces` int(11) NOT NULL DEFAULT 0,
  `rut` varchar(12) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `tipo_moneda` enum('CLP','USD','EUR') NOT NULL DEFAULT 'CLP',
  `id_comuna` int(11) DEFAULT NULL,
  `id_banco` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `usuario`, `contrasena`, `saldo`, `dulces`, `rut`, `direccion`, `tipo_moneda`, `id_comuna`, `id_banco`) VALUES
(1, 'Martin', 'martinys1', 163000, 6, '22446506-8', 'Scottie Scott 589', 'CLP', 48, 3),
(2, 'vicente', 'sayko.exe', 2000, 0, '224307322', 'alejandro soto 025', 'CLP', 48, 3),
(3, 'sebita', 'seba200710', 51612, 6, '22576640-1', 'calle nueva431', 'CLP', 52, 3),
(4, 'tadeo', '123456789', 52500, 0, '225710813', 'av pixulong 235', 'CLP', 48, 1),
(5, 'Renato', 'renato8sigma', 0, 0, '225199418', 'pedro correa ', 'CLP', 52, 1),
(6, 'Amy', 'martinteamo', 30000, 0, '22743879-8', 'Villa el alba Los Cerezos', 'CLP', 49, 3),
(7, 'Kenner', 'sofiateamo', 3100, 0, '28565896-9', 'Villa Cariño', 'CLP', 48, 3),
(8, 'hrod', '123456', 0, 0, '131313131', 'dfgdfg', 'CLP', 49, 3),
(10, 'rolando', 'martingay', 40000, 0, '226153462', 'sada123', 'USD', 41, 5),
(12, 'cheemsito', 'sayko.exe', 0, 0, '22430732-2', 'alejandro soto 025', 'CLP', 48, 3),
(13, 'sebaa', 'sebaa2007', 0, 0, '225766401', 'calle nva431', 'CLP', 52, 3),
(14, 'Tito', '123456', 1397000, 0, '133396691', 'fddf', 'USD', 49, 3),
(15, 'Peter', 'chess', -800, 0, '222900', '1000', 'CLP', 49, 1),
(16, 'ale', 'alison0909/', 991000, 0, '223866778', 'tegualda1156', 'CLP', 4, 2),
(17, 'vicente', 'HOLA12345', 304000, 0, '22386157-1', 'Villa los alamos', 'CLP', 49, 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- Indices de la tabla `bancos`
--
ALTER TABLE `bancos`
  ADD PRIMARY KEY (`id_banco`);

--
-- Indices de la tabla `canjes_dulces`
--
ALTER TABLE `canjes_dulces`
  ADD PRIMARY KEY (`id_canje`),
  ADD KEY `id_admin` (`id_admin`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `comunas`
--
ALTER TABLE `comunas`
  ADD PRIMARY KEY (`id_comuna`);

--
-- Indices de la tabla `historial_partidas`
--
ALTER TABLE `historial_partidas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_juego` (`id_juego`);

--
-- Indices de la tabla `juegos`
--
ALTER TABLE `juegos`
  ADD PRIMARY KEY (`id_juego`);

--
-- Indices de la tabla `transacciones`
--
ALTER TABLE `transacciones`
  ADD PRIMARY KEY (`id_transaccion`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_banco` (`id_banco`),
  ADD KEY `fk_transaccion_canje` (`id_canje`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `rut` (`rut`),
  ADD KEY `id_comuna` (`id_comuna`),
  ADD KEY `id_banco` (`id_banco`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administradores`
--
ALTER TABLE `administradores`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `bancos`
--
ALTER TABLE `bancos`
  MODIFY `id_banco` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `canjes_dulces`
--
ALTER TABLE `canjes_dulces`
  MODIFY `id_canje` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `comunas`
--
ALTER TABLE `comunas`
  MODIFY `id_comuna` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT de la tabla `historial_partidas`
--
ALTER TABLE `historial_partidas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=410;

--
-- AUTO_INCREMENT de la tabla `juegos`
--
ALTER TABLE `juegos`
  MODIFY `id_juego` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `transacciones`
--
ALTER TABLE `transacciones`
  MODIFY `id_transaccion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `canjes_dulces`
--
ALTER TABLE `canjes_dulces`
  ADD CONSTRAINT `canjes_dulces_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `administradores` (`id_admin`),
  ADD CONSTRAINT `canjes_dulces_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `historial_partidas`
--
ALTER TABLE `historial_partidas`
  ADD CONSTRAINT `historial_partidas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `historial_partidas_ibfk_2` FOREIGN KEY (`id_juego`) REFERENCES `juegos` (`id_juego`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `transacciones`
--
ALTER TABLE `transacciones`
  ADD CONSTRAINT `fk_transaccion_canje` FOREIGN KEY (`id_canje`) REFERENCES `canjes_dulces` (`id_canje`),
  ADD CONSTRAINT `transacciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `transacciones_ibfk_2` FOREIGN KEY (`id_banco`) REFERENCES `bancos` (`id_banco`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_comuna`) REFERENCES `comunas` (`id_comuna`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`id_banco`) REFERENCES `bancos` (`id_banco`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
