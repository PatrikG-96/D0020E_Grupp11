-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Värd: 127.0.0.1
-- Tid vid skapande: 23 feb 2022 kl 11:12
-- Serverversion: 10.4.21-MariaDB
-- PHP-version: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Databas: `d0020e_dev`
--

-- --------------------------------------------------------

--
-- Tabellstruktur `action`
--

CREATE TABLE `action` (
  `userID` int(11) NOT NULL,
  `alarmID` int(11) NOT NULL,
  `actionType` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Tabellstruktur `actiontype`
--

CREATE TABLE `actiontype` (
  `actionTypeID` int(11) NOT NULL,
  `nameType` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumpning av Data i tabell `actiontype`
--

INSERT INTO `actiontype` (`actionTypeID`, `nameType`) VALUES
(1, 'read'),
(2, 'solved');

-- --------------------------------------------------------

--
-- Tabellstruktur `alarm`
--

CREATE TABLE `alarm` (
  `alarmID` int(11) NOT NULL,
  `monitorID` int(11) NOT NULL,
  `alarmType` int(11) NOT NULL,
  `read` int(11) NOT NULL,
  `resolved` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Tabellstruktur `alarmtype`
--

CREATE TABLE `alarmtype` (
  `alarmTypeID` int(11) NOT NULL,
  `nameType` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumpning av Data i tabell `alarmtype`
--

INSERT INTO `alarmtype` (`alarmTypeID`, `nameType`) VALUES
(1, 'fall'),
(2, 'fall_confirmed');

-- --------------------------------------------------------

--
-- Tabellstruktur `endpoints`
--

CREATE TABLE `endpoints` (
  `id` int(11) NOT NULL,
  `endpoint` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`endpoint`)),
  `userID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellstruktur `monitor`
--

CREATE TABLE `monitor` (
  `monitorID` int(11) NOT NULL,
  `name` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellstruktur `sensor`
--

CREATE TABLE `sensor` (
  `deviceID` int(11) NOT NULL,
  `monitorID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumpning av Data i tabell `sensor`
--

-- --------------------------------------------------------

--
-- Tabellstruktur `subscription`
--

CREATE TABLE `subscription` (
  `subID` int(11) NOT NULL,
  `userID` int(11) NOT NULL,
  `monitorID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Tabellstruktur `user`
--

CREATE TABLE `user` (
  `userID` int(11) NOT NULL,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `role` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Index för dumpade tabeller
--

--
-- Index för tabell `action`
--
ALTER TABLE `action`
  ADD PRIMARY KEY (`userID`,`alarmID`,`actionType`),
  ADD KEY `fk7` (`alarmID`),
  ADD KEY `fk8` (`actionType`);

--
-- Index för tabell `actiontype`
--
ALTER TABLE `actiontype`
  ADD PRIMARY KEY (`actionTypeID`);

--
-- Index för tabell `alarm`
--
ALTER TABLE `alarm`
  ADD PRIMARY KEY (`alarmID`),
  ADD KEY `fk4` (`monitorID`),
  ADD KEY `fk5` (`alarmType`);

--
-- Index för tabell `alarmtype`
--
ALTER TABLE `alarmtype`
  ADD PRIMARY KEY (`alarmTypeID`);

--
-- Index för tabell `endpoints`
--
ALTER TABLE `endpoints`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_userID_idx` (`userID`);

--
-- Index för tabell `monitor`
--
ALTER TABLE `monitor`
  ADD PRIMARY KEY (`monitorID`);

--
-- Index för tabell `sensor`
--
ALTER TABLE `sensor`
  ADD PRIMARY KEY (`deviceID`),
  ADD KEY `fk1` (`monitorID`);

--
-- Index för tabell `subscription`
--
ALTER TABLE `subscription`
  ADD PRIMARY KEY (`subID`),
  ADD KEY `fk2` (`userID`),
  ADD KEY `fk3` (`monitorID`);

--
-- Index för tabell `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userID`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT för dumpade tabeller
--

--
-- AUTO_INCREMENT för tabell `actiontype`
--
ALTER TABLE `actiontype`
  MODIFY `actionTypeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT för tabell `alarm`
--
ALTER TABLE `alarm`
  MODIFY `alarmID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT för tabell `alarmtype`
--
ALTER TABLE `alarmtype`
  MODIFY `alarmTypeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT för tabell `endpoints`
--
ALTER TABLE `endpoints`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT för tabell `monitor`
--
ALTER TABLE `monitor`
  MODIFY `monitorID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT för tabell `sensor`
--
ALTER TABLE `sensor`
  MODIFY `deviceID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT för tabell `subscription`
--
ALTER TABLE `subscription`
  MODIFY `subID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT för tabell `user`
--
ALTER TABLE `user`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restriktioner för dumpade tabeller
--

--
-- Restriktioner för tabell `action`
--
ALTER TABLE `action`
  ADD CONSTRAINT `fk6` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`),
  ADD CONSTRAINT `fk7` FOREIGN KEY (`alarmID`) REFERENCES `alarm` (`alarmID`),
  ADD CONSTRAINT `fk8` FOREIGN KEY (`actionType`) REFERENCES `actiontype` (`actionTypeID`);

--
-- Restriktioner för tabell `alarm`
--
ALTER TABLE `alarm`
  ADD CONSTRAINT `fk4` FOREIGN KEY (`monitorID`) REFERENCES `monitor` (`monitorID`),
  ADD CONSTRAINT `fk5` FOREIGN KEY (`alarmType`) REFERENCES `alarmtype` (`alarmTypeID`);

--
-- Restriktioner för tabell `endpoints`
--
ALTER TABLE `endpoints`
  ADD CONSTRAINT `fk_userID` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Restriktioner för tabell `sensor`
--
ALTER TABLE `sensor`
  ADD CONSTRAINT `fk1` FOREIGN KEY (`monitorID`) REFERENCES `monitor` (`monitorID`);

--
-- Restriktioner för tabell `subscription`
--
ALTER TABLE `subscription`
  ADD CONSTRAINT `fk2` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`),
  ADD CONSTRAINT `fk3` FOREIGN KEY (`monitorID`) REFERENCES `monitor` (`monitorID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
