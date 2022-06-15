-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 15 Jun 2022 pada 15.03
-- Versi server: 10.4.22-MariaDB
-- Versi PHP: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `morse`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `kode_morse`
--

CREATE TABLE `kode_morse` (
  `Kode` varchar(10) NOT NULL,
  `Karakter` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `kode_morse`
--

INSERT INTO `kode_morse` (`Kode`, `Karakter`) VALUES
('.-', 'a'),
('-...', 'b'),
('-.-.', 'c'),
('-..', 'd'),
('.', 'e'),
('..-.', 'f'),
('--.', 'g'),
('....', 'h'),
('..', 'i'),
('.---', 'j'),
('-.-', 'k'),
('.-..', 'l'),
('--', 'm'),
('-.', 'n'),
('---', 'o'),
('.--.', 'p'),
('--.-', 'q'),
('.-.', 'r'),
('...', 's'),
('-', 't'),
('..-', 'u'),
('...-', 'v'),
('.--', 'w'),
('-..-', 'x'),
('-.--', 'y'),
('--..', 'z'),
('-----', '0'),
('.----', '1'),
('..---', '2'),
('...--', '3'),
('....-', '4'),
('.....', '5'),
('-....', '6'),
('--...', '7'),
('---..', '8'),
('----.', '9'),
('.-.-.-', '.'),
('--..--', ','),
('..--..', '?'),
('-.-.--', '!'),
('.----.', '\''),
('.-..-.', '\"'),
('-.--.', '('),
('-.--.-', ')'),
('.-...', '&'),
('---...', ':'),
('-.-.-.', ';'),
('-..-.', '/'),
('..--.-', '_'),
('-...-', '='),
('.-.-.', '+'),
('-....-', '-'),
('...-..-', '$'),
('.--.-.', '@');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
