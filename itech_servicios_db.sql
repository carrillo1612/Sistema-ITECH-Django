-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 25-11-2025 a las 22:40:38
-- Versión del servidor: 8.4.7
-- Versión de PHP: 8.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `itech_servicios_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividades`
--

DROP TABLE IF EXISTS `actividades`;
CREATE TABLE IF NOT EXISTS `actividades` (
  `ActividadID` int NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(255) DEFAULT NULL,
  `ClienteID` int DEFAULT NULL,
  `Descripcion` text,
  `Fecha` date DEFAULT NULL,
  `Inicio` time DEFAULT NULL,
  `Fin` time DEFAULT NULL,
  `PersonalAsignadoID` int DEFAULT NULL,
  `Estado` varchar(50) DEFAULT NULL,
  `Ubicacion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ActividadID`),
  KEY `ClienteID` (`ClienteID`),
  KEY `PersonalAsignadoID` (`PersonalAsignadoID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add usuarios', 1, 'add_usuarios'),
(2, 'Can change usuarios', 1, 'change_usuarios'),
(3, 'Can delete usuarios', 1, 'delete_usuarios'),
(4, 'Can view usuarios', 1, 'view_usuarios'),
(5, 'Can add clientes', 2, 'add_clientes'),
(6, 'Can change clientes', 2, 'change_clientes'),
(7, 'Can delete clientes', 2, 'delete_clientes'),
(8, 'Can view clientes', 2, 'view_clientes'),
(9, 'Can add actividades', 3, 'add_actividades'),
(10, 'Can change actividades', 3, 'change_actividades'),
(11, 'Can delete actividades', 3, 'delete_actividades'),
(12, 'Can view actividades', 3, 'view_actividades'),
(13, 'Can add ordenes servicio', 4, 'add_ordenesservicio'),
(14, 'Can change ordenes servicio', 4, 'change_ordenesservicio'),
(15, 'Can delete ordenes servicio', 4, 'delete_ordenesservicio'),
(16, 'Can view ordenes servicio', 4, 'view_ordenesservicio'),
(17, 'Can add orden detalles', 5, 'add_ordendetalles'),
(18, 'Can change orden detalles', 5, 'change_ordendetalles'),
(19, 'Can delete orden detalles', 5, 'delete_ordendetalles'),
(20, 'Can view orden detalles', 5, 'view_ordendetalles'),
(21, 'Can add registros tecnicos', 6, 'add_registrostecnicos'),
(22, 'Can change registros tecnicos', 6, 'change_registrostecnicos'),
(23, 'Can delete registros tecnicos', 6, 'delete_registrostecnicos'),
(24, 'Can view registros tecnicos', 6, 'view_registrostecnicos'),
(25, 'Can add registro fotos', 7, 'add_registrofotos'),
(26, 'Can change registro fotos', 7, 'change_registrofotos'),
(27, 'Can delete registro fotos', 7, 'delete_registrofotos'),
(28, 'Can view registro fotos', 7, 'view_registrofotos'),
(29, 'Can add log entry', 8, 'add_logentry'),
(30, 'Can change log entry', 8, 'change_logentry'),
(31, 'Can delete log entry', 8, 'delete_logentry'),
(32, 'Can view log entry', 8, 'view_logentry'),
(33, 'Can add permission', 10, 'add_permission'),
(34, 'Can change permission', 10, 'change_permission'),
(35, 'Can delete permission', 10, 'delete_permission'),
(36, 'Can view permission', 10, 'view_permission'),
(37, 'Can add group', 11, 'add_group'),
(38, 'Can change group', 11, 'change_group'),
(39, 'Can delete group', 11, 'delete_group'),
(40, 'Can view group', 11, 'view_group'),
(41, 'Can add content type', 9, 'add_contenttype'),
(42, 'Can change content type', 9, 'change_contenttype'),
(43, 'Can delete content type', 9, 'delete_contenttype'),
(44, 'Can view content type', 9, 'view_contenttype'),
(45, 'Can add session', 12, 'add_session'),
(46, 'Can change session', 12, 'change_session'),
(47, 'Can delete session', 12, 'delete_session'),
(48, 'Can view session', 12, 'view_session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `ClienteID` int NOT NULL AUTO_INCREMENT,
  `NombreComercial` varchar(255) NOT NULL,
  `Telefono` varchar(20) DEFAULT NULL,
  `Correo` varchar(255) DEFAULT NULL,
  `Calle` varchar(255) DEFAULT NULL,
  `NumeroExterior` varchar(20) DEFAULT NULL,
  `Interior` varchar(20) DEFAULT NULL,
  `Colonia` varchar(100) DEFAULT NULL,
  `CodigoPostal` varchar(10) DEFAULT NULL,
  `Ciudad` varchar(100) DEFAULT NULL,
  `Pais` varchar(100) DEFAULT NULL,
  `Ubicacion` longtext,
  PRIMARY KEY (`ClienteID`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`ClienteID`, `NombreComercial`, `Telefono`, `Correo`, `Calle`, `NumeroExterior`, `Interior`, `Colonia`, `CodigoPostal`, `Ciudad`, `Pais`, `Ubicacion`) VALUES
(1, 'ELIZA MENDEZ SANCHEZ', '9335691241', 'NA@GMAIL', 'COCOHITE', 'SN', 'SN', 'XOCHIMILCO', 'SN', 'Tabasco', 'México', 'https://maps.app.goo.gl/1fJXUsner4LedzsXA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'servicios', 'usuarios'),
(2, 'servicios', 'clientes'),
(3, 'servicios', 'actividades'),
(4, 'servicios', 'ordenesservicio'),
(5, 'servicios', 'ordendetalles'),
(6, 'servicios', 'registrostecnicos'),
(7, 'servicios', 'registrofotos'),
(8, 'admin', 'logentry'),
(9, 'contenttypes', 'contenttype'),
(10, 'auth', 'permission'),
(11, 'auth', 'group'),
(12, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'servicios', '0001_initial', '2025-11-19 05:20:42.488124'),
(2, 'contenttypes', '0001_initial', '2025-11-19 05:20:42.498043'),
(3, 'admin', '0001_initial', '2025-11-19 05:20:42.525946'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-19 05:20:42.545952'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-19 05:20:42.557866'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-11-19 05:21:56.069543'),
(7, 'auth', '0001_initial', '2025-11-19 05:30:33.550383'),
(8, 'auth', '0002_alter_permission_name_max_length', '2025-11-19 05:30:33.687203'),
(9, 'auth', '0003_alter_user_email_max_length', '2025-11-19 05:30:33.701512'),
(10, 'auth', '0004_alter_user_username_opts', '2025-11-19 05:30:33.728150'),
(11, 'auth', '0005_alter_user_last_login_null', '2025-11-19 05:30:33.750655'),
(12, 'auth', '0006_require_contenttypes_0002', '2025-11-19 05:30:33.752190'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2025-11-19 05:30:33.765748'),
(14, 'auth', '0008_alter_user_username_max_length', '2025-11-19 05:30:33.773047'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2025-11-19 05:30:33.788070'),
(16, 'auth', '0010_alter_group_name_max_length', '2025-11-19 05:30:33.880770'),
(17, 'auth', '0011_update_proxy_permissions', '2025-11-19 05:30:33.902697'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2025-11-19 05:30:33.913633'),
(19, 'servicios', '0002_alter_clientes_ubicacion', '2025-11-19 05:30:46.564481'),
(20, 'sessions', '0001_initial', '2025-11-19 05:30:46.569353'),
(21, 'servicios', '0003_alter_ordenesservicio_giro', '2025-11-23 02:57:00.632747'),
(22, 'servicios', '0004_ordenesservicio_fin_ordenesservicio_inicio', '2025-11-23 06:07:09.650539');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('7b376t57ebdbvxsbftijux4wcnpir743', '.eJxVjMsKwjAQAP9lzxLibsijR-9-Q8hmE1OVFpr2VPx3KfSg15lhdohpW1vcelniKDCAh8sv45RfZTqEPNP0mFWep3UZWR2JOm1X91nK-3a2f4OWeoMBkCwnyc5l9liZMhUx1UglRtaayXvjKGgSG65YE2vjAqJ1FTnkoOHzBftcN9M:1vLaBT:6XO24fXnzhe1FXIkF03c6owqm_QmEy4e0_GlhZRUU20', '2025-12-03 04:52:47.184787'),
('0byx2f6bqp4998spet6nbygcaf3kn3px', '.eJxVjMsKwjAQAP9lzxLibsijR-9-Q8hmE1OVFpr2VPx3KfSg15lhdohpW1vcelniKDCAh8sv45RfZTqEPNP0mFWep3UZWR2JOm1X91nK-3a2f4OWeoMBkCwnyc5l9liZMhUx1UglRtaayXvjKGgSG65YE2vjAqJ1FTnkoOHzBftcN9M:1vKsDL:8jdQmoOuME7SkNwfUoXYhHv6YY60szR_pEPNbKfsX6E', '2025-12-01 05:55:47.237395'),
('ryqzoyg1s44zvclydviourhn8puy0m82', '.eJxVjM0OwiAQhN-FsyH8CAWP3n0GsuwuUjU0Ke3J-O62SQ96m8z3zbxFgnWpae08p5HERThx-u0y4JPbDugB7T5JnNoyj1nuijxol7eJ-HU93L-DCr1uaw5BD8oUG1BvYSCrjCfWJkYkF4l8OWtPlnRUlpwNlDUiQuEAJrASny_J4zfV:1vLlXE:EznmVj95NlZuqH-lsleiCjTlBH2L_gI16tWjDzPuSRU', '2025-12-03 17:00:00.383637'),
('j6s7sg9156c7igkr4evkiqrlazsyvgnc', '.eJxVjEEOwiAQAP-yZ0NYsAV69N43ELq7SNXQpLQn499Nkx70OjOZN8S0byXuTdY4MwzQweWXTYmeUg_Bj1Tvi6Klbus8qSNRp21qXFhet7P9G5TUCgwg3qPTJltPiE47ttr0LGhCIO4Cc5-v2LNlDNpyZz1PSEQpi0_Gi4bPF8njN9U:1vN0Jk:4sxAJGxCqzApXUvsyOj8JoQmHtJipOzJaBqynKoPuXE', '2025-12-07 02:59:12.947736'),
('e36xpmpagqxer12wnih7ojng5vi358zm', '.eJxVjMsOgjAQAP9lz6bpwrptOXrnG5o-FouaklA4Gf_dkHDQ68xk3uDDvhW_N1n9nGEAA5dfFkN6Sj1EfoR6X1Ra6rbOUR2JOm1T45LldTvbv0EJrcAAbIlJmDWlODnKiJ3Gq2EWwRw5aQmBNEYTBXtreGLtEC1R12d0BuHzBcWkNq4:1vNRbw:5fUY2IAP9eAPKTiICdg-JdGeYmyNj1KujMaK1yFeifA', '2025-12-08 08:07:48.785071'),
('f3qdkslntough0wgp02r7g6glzfngq6i', '.eJxVjDEOgzAMAP_iuYpMGhPD2J03IOM4hbYCicBU9e8VEkO73p3uDb3s29jvxdZ-StBCBZdfNog-bT5Eesh8X5wu87ZOgzsSd9riuiXZ63a2f4NRyggtWE5E6pscPWHmHNhrrCV6U094NaZIhhSEG48V1ojJQkaNwoMoJ_h8Adh6N6U:1vNle0:vgFlhj8gf5bJzk3RCeM-rjw7RYIzZZYnAa8_JHmTO-0', '2025-12-09 05:31:16.311749'),
('k8m58rsnkrf7v2wwpldv3ol8evqx5ls6', '.eJxVjMsOwiAQRf-FtSE8phVcuvcbyAwwUjWQlHZl_HdD0oVu7znnvkXAfSth73kNSxIXYcXpdyOMz1wHSA-s9yZjq9u6kByKPGiXt5by63q4fwcFexm1twQJHMDsOJOOCKhJqQgeo3czA6DyaKI3erLGT9kwE7NVZM-oQXy-6lY3-A:1vNvKh:GsIgKxY4dl_TNmWKRG7DTNs0yciAzrq3hVNNiuoIh-k', '2025-12-09 15:51:59.723525'),
('o1rpkrtafktl9z0uqndtwhcj4okkrneu', '.eJxVjDEOgzAMAP_iuYpCSGzC2L1viJzYFNoKJAJT1b9XSAztene6NyTetzHtVdc0CfTg4PLLMpenzoeQB8_3xZRl3tYpmyMxp63mtoi-rmf7Nxi5jtCDkhDGtrES0EYXeAjsbSbHTWZ1PhTbdkLoufhOOKK6QZCIULJSGeDzBdRsOAw:1vNvYw:N285gTHTg8jzrcolIKjdsACLSX_xayh-VxQMmP-oAWM', '2025-12-09 16:06:42.711595');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordendetalles`
--

DROP TABLE IF EXISTS `ordendetalles`;
CREATE TABLE IF NOT EXISTS `ordendetalles` (
  `DetalleID` int NOT NULL AUTO_INCREMENT,
  `OrdenID` int DEFAULT NULL,
  `Cantidad` int DEFAULT NULL,
  `Producto` varchar(255) DEFAULT NULL,
  `InformacionAdicional` text,
  PRIMARY KEY (`DetalleID`),
  KEY `OrdenID` (`OrdenID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `ordendetalles`
--

INSERT INTO `ordendetalles` (`DetalleID`, `OrdenID`, `Cantidad`, `Producto`, `InformacionAdicional`) VALUES
(1, 1, 1, 'MINISPLIT MIRAGE', '1 TONELADA 12BTU 220 MODELO NEX'),
(2, 2, 1, 'Clima', '2');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenesservicio`
--

DROP TABLE IF EXISTS `ordenesservicio`;
CREATE TABLE IF NOT EXISTS `ordenesservicio` (
  `OrdenID` int NOT NULL AUTO_INCREMENT,
  `ClienteEmpresaID` int DEFAULT NULL,
  `TelefonoContacto` varchar(20) DEFAULT NULL,
  `EmailContacto` varchar(255) DEFAULT NULL,
  `Servicio` varchar(255) DEFAULT NULL,
  `PersonalAsignadoID` int DEFAULT NULL,
  `Giro` varchar(100) DEFAULT NULL,
  `Ubicacion` varchar(255) DEFAULT NULL,
  `FallaReportada` text,
  `Programada` datetime DEFAULT NULL,
  `Precio` decimal(10,2) DEFAULT NULL,
  `Estado` varchar(50) NOT NULL,
  `Fin` time(6) DEFAULT NULL,
  `Inicio` time(6) DEFAULT NULL,
  PRIMARY KEY (`OrdenID`),
  KEY `ClienteEmpresaID` (`ClienteEmpresaID`),
  KEY `PersonalAsignadoID` (`PersonalAsignadoID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `ordenesservicio`
--

INSERT INTO `ordenesservicio` (`OrdenID`, `ClienteEmpresaID`, `TelefonoContacto`, `EmailContacto`, `Servicio`, `PersonalAsignadoID`, `Giro`, `Ubicacion`, `FallaReportada`, `Programada`, `Precio`, `Estado`, `Fin`, `Inicio`) VALUES
(1, 1, '9335691241', 'NA@GMAIL', 'Instalación', 3, 'Servicios residencial', 'https://maps.app.goo.gl/1fJXUsner4LedzsXA', 'SE REALIZARA INSTALACION', '2025-11-25 15:47:00', 0.00, 'Terminada', '09:58:51.017790', '09:53:07.223664'),
(2, 1, '9335691241', 'NA@GMAIL', 'Mantenimiento', 3, 'Energia', 'https://maps.app.goo.gl/1fJXUsner4LedzsXA', 'Fallas', '2025-11-25 16:07:00', 2000.00, 'Terminada', '10:10:38.321491', '10:07:34.302324');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registrofotos`
--

DROP TABLE IF EXISTS `registrofotos`;
CREATE TABLE IF NOT EXISTS `registrofotos` (
  `FotoID` int NOT NULL AUTO_INCREMENT,
  `Imagen` varchar(100) NOT NULL,
  `Descripcion` text NOT NULL,
  `Registro_id` int NOT NULL,
  PRIMARY KEY (`FotoID`),
  KEY `registrofotos_Registro_id_fk` (`Registro_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `registrofotos`
--

INSERT INTO `registrofotos` (`FotoID`, `Imagen`, `Descripcion`, `Registro_id`) VALUES
(1, 'fotos/registros/OIP_1_NEJldab.webp', 'CLIMA COLOCADO', 1),
(2, 'fotos/registros/OIP_9RkyoUB.webp', 'CLIMA COLOCADO', 1),
(3, 'fotos/registros/cr7-hd-name-x3109jkxnxrm6w73_fypJBRI.jpg', 'CLIMA COLOCADO', 1),
(4, 'fotos/registros/5c4a7855b62325277b833cd4b317b29d.jpg', 'CLIMA COLOCADO', 1),
(5, 'fotos/registros/71QKVtKTbdL._AC_SL1500_.jpg', 'CLIMA COLOCADO', 1),
(6, 'fotos/registros/2b906386df5031a2c009e0f380da2e74_jBXmaZh.jpg', 'CLIMA COLOCADO', 1),
(7, 'fotos/registros/83b811e59b98b9c63669b070463e7d6c.jpg', 'CLIMA COLOCADO', 1),
(8, 'fotos/registros/1408248_QdMXr40.jpg', 'CLIMA COLOCADO', 1),
(9, 'fotos/registros/Ima_V5bq0zh.jpg', 'CLIMA COLOCADO', 1),
(10, 'fotos/registros/5.jpg', 'C', 2),
(11, 'fotos/registros/4.jpg', 'C', 2),
(12, 'fotos/registros/3.jpg', 'C', 2),
(13, 'fotos/registros/1.jpg', 'C', 2),
(14, 'fotos/registros/2.jpg', 'C', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registrostecnicos`
--

DROP TABLE IF EXISTS `registrostecnicos`;
CREATE TABLE IF NOT EXISTS `registrostecnicos` (
  `RegistroID` int NOT NULL AUTO_INCREMENT,
  `OrdenID` int NOT NULL,
  `TipoUnidad` varchar(100) DEFAULT NULL,
  `Marca` varchar(100) DEFAULT NULL,
  `Modelo` varchar(100) DEFAULT NULL,
  `Capacidad` varchar(100) DEFAULT NULL,
  `TipoGasRefrigerante` varchar(50) DEFAULT NULL,
  `InstalacionCondensador` varchar(100) DEFAULT NULL,
  `ServicioRealizado` varchar(255) DEFAULT NULL,
  `DistanciaEvap` varchar(50) DEFAULT NULL,
  `DistanciaAlimentacion` varchar(50) DEFAULT NULL,
  `CalibreCableado` varchar(50) DEFAULT NULL,
  `TamanoHabitacion` varchar(50) DEFAULT NULL,
  `Desague` varchar(100) DEFAULT NULL,
  `PresionGasRefrig` varchar(50) DEFAULT NULL,
  `VoltajeAlimentacion` varchar(50) DEFAULT NULL,
  `VoltajeTerminalesCond` varchar(50) DEFAULT NULL,
  `TempHabitacion` varchar(50) DEFAULT NULL,
  `TempDescarga` varchar(50) DEFAULT NULL,
  `BombaVacio` varchar(50) DEFAULT NULL,
  `TiempoVacio` varchar(50) DEFAULT NULL,
  `CapacitorCompresor_Original` varchar(50) DEFAULT NULL,
  `CapacitorCompresor_Actual` varchar(50) DEFAULT NULL,
  `CapacitorVentilador_Original` varchar(50) DEFAULT NULL,
  `CapacitorVentilador_Actual` varchar(50) DEFAULT NULL,
  `AmpTerminalesCompresor_Original` varchar(50) DEFAULT NULL,
  `AmpTerminalesCompresor_Actual` varchar(50) DEFAULT NULL,
  `SensorPozo_Original` varchar(50) DEFAULT NULL,
  `SensorPozo_Actual` varchar(50) DEFAULT NULL,
  `SensorAmbiente_Original` varchar(50) DEFAULT NULL,
  `SensorAmbiente_Actual` varchar(50) DEFAULT NULL,
  `TecnicoID` int DEFAULT NULL,
  `ObservacionesTexto` longtext,
  `Satisfaccion` int DEFAULT NULL,
  `ComentarioCliente` longtext,
  `NotasInternas` longtext,
  `MaterialesUtilizados` json DEFAULT NULL,
  `FirmaCliente` varchar(100) DEFAULT NULL,
  `FirmaTecnico` varchar(100) DEFAULT NULL,
  `FechaCreacion` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`RegistroID`),
  UNIQUE KEY `OrdenID` (`OrdenID`),
  KEY `FK_RegistrosTecnicos_Usuarios` (`TecnicoID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `registrostecnicos`
--

INSERT INTO `registrostecnicos` (`RegistroID`, `OrdenID`, `TipoUnidad`, `Marca`, `Modelo`, `Capacidad`, `TipoGasRefrigerante`, `InstalacionCondensador`, `ServicioRealizado`, `DistanciaEvap`, `DistanciaAlimentacion`, `CalibreCableado`, `TamanoHabitacion`, `Desague`, `PresionGasRefrig`, `VoltajeAlimentacion`, `VoltajeTerminalesCond`, `TempHabitacion`, `TempDescarga`, `BombaVacio`, `TiempoVacio`, `CapacitorCompresor_Original`, `CapacitorCompresor_Actual`, `CapacitorVentilador_Original`, `CapacitorVentilador_Actual`, `AmpTerminalesCompresor_Original`, `AmpTerminalesCompresor_Actual`, `SensorPozo_Original`, `SensorPozo_Actual`, `SensorAmbiente_Original`, `SensorAmbiente_Actual`, `TecnicoID`, `ObservacionesTexto`, `Satisfaccion`, `ComentarioCliente`, `NotasInternas`, `MaterialesUtilizados`, `FirmaCliente`, `FirmaTecnico`, `FechaCreacion`) VALUES
(1, 1, 'Sistemassplits', 'MIRAGE', 'NEX', '12 BTU', 'R410', 'Techo', 'Instalacion', '4', '3', 'NA', '12', 'Jardín', '45', '115', '112', '0', '0', '3', '30', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 3, 'SE REALIZO LA INSTALACION', 10, 'EL SERVICIO FUE REALIZADO ADECUADAMENTE', 'TUVIMOS DETALLES', '[]', 'firmas/clientes/cliente_1.png', 'firmas/tecnicos/tecnico_1.png', '2025-11-25 15:58:50.952660'),
(2, 2, 'Sistemassplits', 'MIRAGE', 'NEX', '12 BTU', 'R410', 'Mensulas', 'Mantenimiento', '4', '3', 'NA', '12', 'Jardín', '45', '115', '112', '0', '0', '3', '30', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 3, 'DFGHGJHK', 9, 'ADSA', 'FSDF', '[]', 'firmas/clientes/cliente_2_oykQhyg.png', 'firmas/tecnicos/tecnico_2_jtdm1On.png', '2025-11-25 16:10:38.294515');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `UsuarioID` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(100) DEFAULT NULL,
  `Apellido` varchar(100) DEFAULT NULL,
  `NumeroTelefono` varchar(20) DEFAULT NULL,
  `CorreoElectronico` varchar(191) NOT NULL,
  `Rol` varchar(50) DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`UsuarioID`),
  UNIQUE KEY `CorreoElectronico` (`CorreoElectronico`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`UsuarioID`, `Nombre`, `Apellido`, `NumeroTelefono`, `CorreoElectronico`, `Rol`, `password`, `last_login`, `is_active`) VALUES
(1, 'Carlos Alberto', 'Carrillo Solano', '9331575159', 'carlosalbertocarrillosolano@gmail.com', 'Administrador', 'pbkdf2_sha256$1000000$acWdjbS8pyRoETg1EwNAzm$pHXMJ3W7qb2bOJwXXchLsgOLe3V/o1mlwX2YWPnyQGU=', '2025-11-25 15:36:43', 1),
(2, 'KARINA', 'RICARDEZ', '9331129250', 'servicios@i-techmx.com', 'Administrador', 'pbkdf2_sha256$1000000$cNhtDiDxxudBVGYFHeO8C2$c5FceLXfmVcSbQFLC9j+0n6WNGhEdpVlnuY7/Sgqu6c=', '2025-11-25 16:06:43', 1),
(3, 'DIEGO', 'DE LOS SANTOS', '9331112222', 'rodriguezhernandezedgar05@gmail.com', 'Técnico', 'pbkdf2_sha256$1000000$NUHSsuWT0OiVKT8RggSLQ6$Xw7fqfF3kX3Er5Lwb/TNwPLfiJJJCte7Da4zeHyWYxI=', '2025-11-25 15:52:00', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
