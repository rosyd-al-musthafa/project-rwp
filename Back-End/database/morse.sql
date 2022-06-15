-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 15 Jun 2022 pada 15.00
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

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat`
--

CREATE TABLE `riwayat` (
  `id` int(11) NOT NULL,
  `bentuk awal` text NOT NULL,
  `terjemahan` text NOT NULL,
  `waktu` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id` tinyint(3) NOT NULL,
  `status` enum('admin','client') NOT NULL DEFAULT 'client',
  `nama` varchar(127) NOT NULL,
  `gender` enum('L','P') NOT NULL,
  `username` varchar(63) NOT NULL,
  `password` varbinary(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `status`, `nama`, `gender`, `username`, `password`) VALUES
(1, 'admin', 'Rosyd Al Musthafa', 'L', 'rosyd', 0x243262243132247671612e342f48337334623870426270642e72446265347962516f394d525664764f3073632f7545436253594e6d6a48436c453761),
(2, 'admin', 'Yusuf Hidayat', 'L', 'you', 0x24326224313224764d564c52694a48663856595163384b635156756a4f783735555971775a57667552695a412e6a6f595a79716b35774a3536796732),
(3, 'client', 'Nur Adelia', 'P', 'adel', 0x2432622431322445314b32534457644141502e7161516d645076626a4f714e356b35705835767567417747594d527261337374452f79536b504c3275),
(4, 'client', 'Hayati', 'P', 'hayati', 0x24326224313224353242424b4e2e2f51754264365961453344303434654e78546b4f487066514335684c4b775659725a454e38656133765039325269),
(5, 'client', 'Reni Ramadhani', 'P', 'ramad', 0x24326224313224363271474d635653473751633231383948467945302e793157472e3472556c49775a4e57527a327434706f35636674543651784a53);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `riwayat`
--
ALTER TABLE `riwayat`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `riwayat`
--
ALTER TABLE `riwayat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` tinyint(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
