-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 12 oct. 2023 à 01:32
-- Version du serveur : 5.7.36
-- Version de PHP : 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `proj`
--

-- --------------------------------------------------------

--
-- Structure de la table `comm_fact`
--

DROP TABLE IF EXISTS `comm_fact`;
CREATE TABLE IF NOT EXISTS `comm_fact` (
  `Id_Commande` varchar(8) NOT NULL,
  `Id_Facture` varchar(8) NOT NULL,
  UNIQUE KEY `Id_Commande` (`Id_Commande`),
  KEY `Id_Facture` (`Id_Facture`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `facture`
--

DROP TABLE IF EXISTS `facture`;
CREATE TABLE IF NOT EXISTS `facture` (
  `Id_Facture` varchar(8) NOT NULL,
  `Produits` varchar(1000) NOT NULL,
  `HT` decimal(8,2) DEFAULT NULL,
  `TTC` decimal(8,2) DEFAULT NULL,
  `Statut` int(11) NOT NULL,
  PRIMARY KEY (`Id_Facture`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `ligne_commande`
--

DROP TABLE IF EXISTS `ligne_commande`;
CREATE TABLE IF NOT EXISTS `ligne_commande` (
  `Id_Commande` varchar(8) NOT NULL,
  `Id_Produit` varchar(8) NOT NULL,
  `Quantite` int(11) NOT NULL,
  `Statut` int(11) NOT NULL,
  PRIMARY KEY (`Id_Commande`),
  KEY `Id_Produit` (`Id_Produit`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `produits`
--

DROP TABLE IF EXISTS `produits`;
CREATE TABLE IF NOT EXISTS `produits` (
  `Id_Produit` varchar(8) NOT NULL,
  `Label` varchar(100) NOT NULL,
  `PU` float NOT NULL,
  `Restants` int(11) NOT NULL,
  PRIMARY KEY (`Id_Produit`),
  UNIQUE KEY `Label` (`Label`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `comm_fact`
--
ALTER TABLE `comm_fact`
  ADD CONSTRAINT `comm_fact_ibfk_1` FOREIGN KEY (`Id_Commande`) REFERENCES `ligne_commande` (`Id_Commande`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `comm_fact_ibfk_2` FOREIGN KEY (`Id_Facture`) REFERENCES `facture` (`Id_Facture`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `ligne_commande`
--
ALTER TABLE `ligne_commande`
  ADD CONSTRAINT `ligne_commande_ibfk_1` FOREIGN KEY (`Id_Produit`) REFERENCES `produits` (`Id_Produit`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
