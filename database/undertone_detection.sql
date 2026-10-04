-- BrownSkin Undertone Detection Database Dump
-- Sesuai untuk MySQL, MariaDB, dan TiDB Cloud

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- --------------------------------------------------------
-- Table structure for table `foundation`
-- --------------------------------------------------------

CREATE TABLE `foundation` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `shade` varchar(100) NOT NULL,
  `skintone` varchar(100) NOT NULL,
  `undertone` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `foundation`
--

INSERT INTO `foundation` (`id`, `shade`, `skintone`, `undertone`) VALUES
(1, 'Milky', 'fair', 'cool'),
(2, 'Milky', 'fair', 'neutral'),
(3, 'Vanilla', 'fair', 'warm'),
(4, 'Milky', 'light medium', 'cool'),
(5, 'Milky', 'light medium', 'neutral'),
(6, 'Vanilla', 'light medium', 'warm'),
(7, 'Latte', 'medium', 'olive'),
(8, 'Butter', 'medium', 'neutral'),
(9, 'Ginger', 'medium', 'warm'),
(10, 'Butter', 'light tan', 'neutral'),
(11, 'Ginger', 'light tan', 'warm'),
(12, 'Latte', 'light tan', 'olive'),
(13, 'Cappucino', 'medium tan', 'warm'),
(14, 'Latte', 'medium tan', 'olive'),
(15, 'Deep Coco', 'tan', 'neutral'),
(16, 'Espresso', 'tan', 'warm'),
(17, 'Deep Coco', 'deep tan', 'neutral'),
(18, 'Espresso', 'deep tan', 'warm');

-- --------------------------------------------------------
-- Table structure for table `lipstick`
-- --------------------------------------------------------

CREATE TABLE `lipstick` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `shade` varchar(100) NOT NULL,
  `skintone` varchar(100) NOT NULL,
  `undertone` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lipstick`
--

INSERT INTO `lipstick` (`id`, `shade`, `skintone`, `undertone`) VALUES
(1, 'it girl', 'fair', 'cool'),
(2, 'it girl', 'medium', 'neutral'),
(3, 'bossy', 'light medium', 'cool'),
(4, 'bossy', 'medium', 'neutral'),
(5, 'timeless', 'fair', 'neutral'),
(6, 'timeless', 'medium', 'warm'),
(7, 'mariam', 'fair', 'cool'),
(8, 'mariam', 'medium', 'neutral'),
(9, 'mariam', 'tan', 'warm'),
(10, 'mariam', 'deep tan', 'warm'),
(11, 'copacabana', 'medium', 'warm'),
(12, 'santorini', 'fair', 'cool'),
(13, 'santorini', 'medium', 'neutral'),
(14, 'santorini', 'tan', 'warm'),
(15, 'santorini', 'deep tan', 'warm'),
(16, 'kuntum', 'medium', 'neutral'),
(17, 'kuntum', 'tan', 'warm'),
(18, 'ratna', 'tan', 'cool'),
(19, 'laila', 'light tan', 'olive'),
(20, 'laila', 'tan', 'warm'),
(21, 'kesuma', 'medium', 'neutral'),
(26, 'GANTI shade light medium warm', 'light medium', 'warm'),
(27, 'GANTI shade medium cool', 'medium', 'cool'),
(28, 'GANTI shade medium olive', 'medium', 'olive'),
(29, 'GANTI shade light tan cool', 'light tan', 'cool'),
(30, 'GANTI shade light tan neutral', 'light tan', 'neutral'),
(31, 'GANTI shade light tan warm', 'light tan', 'warm'),
(32, 'GANTI shade medium tan cool', 'medium tan', 'cool'),
(33, 'GANTI shade medium tan neutral', 'medium tan', 'neutral'),
(34, 'GANTI shade medium tan olive', 'medium tan', 'olive'),
(35, 'GANTI shade medium tan warm', 'medium tan', 'warm'),
(36, 'GANTI shade tan neutral', 'tan', 'neutral'),
(37, 'GANTI shade tan olive', 'tan', 'olive'),
(38, 'GANTI shade deep tan cool', 'deep tan', 'cool'),
(39, 'GANTI shade deep tan neutral', 'deep tan', 'neutral'),
(40, 'GANTI shade deep tan olive', 'deep tan', 'olive');

COMMIT;
