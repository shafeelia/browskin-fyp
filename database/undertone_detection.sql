-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 10, 2026 at 12:07 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `undertone detection`
--

-- --------------------------------------------------------

--
-- Table structure for table `foundation`
--

CREATE TABLE `foundation` (
  `id` int(100) NOT NULL,
  `shade` varchar(100) NOT NULL,
  `skintone` varchar(100) NOT NULL,
  `undertone` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `foundation`
--

INSERT INTO `foundation` (`id`, `shade`, `skintone`, `undertone`) VALUES
(1, 'milky', 'fair', 'cool'),
(2, 'milky', 'fair', 'neutral'),
(3, 'milky', 'fair', 'warm'),
(4, 'milky', 'light medium', 'cool'),
(5, 'milky', 'light medium', 'neutral'),
(6, 'vanilla', 'fair', 'neutral'),
(7, 'vanilla', 'fair', 'warm'),
(8, 'vanilla', 'light medium', 'cool'),
(9, 'vanilla', 'light medium', 'neutral'),
(10, 'vanilla', 'medium', 'neutral'),
(11, 'vanilla', 'medium', 'warm'),
(12, 'butter', 'light medium', 'cool'),
(13, 'butter', 'light medium', 'warm'),
(14, 'butter', 'medium', 'neutral'),
(15, 'butter', 'medium', 'warm'),
(16, 'ginger', 'medium', 'neutral'),
(17, 'ginger', 'medium', 'warm'),
(18, 'latte', 'light tan', 'olive'),
(19, 'latte', 'medium tan', 'olive'),
(20, 'cappucino', 'medium tan', 'warm'),
(21, 'espresso', 'tan', 'warm'),
(22, 'espresso', 'tan', 'olive'),
(23, 'deep coco', 'tan', 'neutral'),
(24, 'deep coco', 'tan', 'warm'),
(25, 'deep coco', 'deep tan', 'neutral'),
(26, 'deep coco', 'deep tan', 'warm'); 

-- --------------------------------------------------------

--
-- Table structure for table `lipstick`
--

CREATE TABLE `lipstick` (
  `id` int(100) NOT NULL,
  `shade` varchar(100) NOT NULL,
  `skintone` varchar(100) NOT NULL,
  `undertone` varchar(100) DEFAULT NULL
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
(21, 'kesuma', 'medium', 'neutral');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `foundation`
--

ALTER TABLE `foundation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `lipstick`
--

ALTER TABLE `lipstick`
  ADD PRIMARY KEY (`id`);


--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `foundation`
--

ALTER TABLE `foundation`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `lipstick`
--

ALTER TABLE `lipstick`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
