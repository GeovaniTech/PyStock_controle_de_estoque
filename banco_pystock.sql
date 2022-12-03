-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Tempo de geração: 19-Abr-2022 às 20:25
-- Versão do servidor: 5.7.31
-- versão do PHP: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `banco_pystock`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `CPF` varchar(255) DEFAULT NULL,
  `Nome` varchar(255) DEFAULT NULL,
  `Endereço` varchar(255) DEFAULT NULL,
  `Contato` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `clientes`
--

INSERT INTO `clientes` (`CPF`, `Nome`, `Endereço`, `Contato`) VALUES
('129.107.059-19', 'Geovani Debastiani', 'R. do Geovani', '(47) 9 9999-9999'),
('000.000.000-00', 'Pedro Fer', 'R. do Pedro', '(00) 0 0000-0000'),
('165.444.456-44', 'Anderson', 'R. do Anderson', '(47) 0 0041-6547');

-- --------------------------------------------------------

--
-- Estrutura da tabela `fornecedores`
--

DROP TABLE IF EXISTS `fornecedores`;
CREATE TABLE IF NOT EXISTS `fornecedores` (
  `Nome` varchar(255) DEFAULT NULL,
  `Endereço` varchar(255) DEFAULT NULL,
  `Contato` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `fornecedores`
--

INSERT INTO `fornecedores` (`Nome`, `Endereço`, `Contato`) VALUES
('Tirol', 'R. da Tirol', '(47) 9 9544-5444'),
('Coca-Cola', 'R. da Coca', '(18) 9 9928-4555'),
('LG', 'R. da LG', '(47) 9 9284-5613'),
('LongaVita', 'R. LongaVita', '(47) 0 0001-1564');

-- --------------------------------------------------------

--
-- Estrutura da tabela `login`
--

DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `usuario` varchar(255) DEFAULT NULL,
  `senha` varchar(255) DEFAULT NULL,
  `nivel` varchar(255) DEFAULT NULL,
  `nome` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `login`
--

INSERT INTO `login` (`usuario`, `senha`, `nivel`, `nome`) VALUES
('GeovaniDebastiani', '123', 'admin', 'Geovani Debastiani'),
('MarcosA', '123', 'colaborador', 'Marcos Antônio');

-- --------------------------------------------------------

--
-- Estrutura da tabela `monitoramento_vendas`
--

DROP TABLE IF EXISTS `monitoramento_vendas`;
CREATE TABLE IF NOT EXISTS `monitoramento_vendas` (
  `vendedor` varchar(255) DEFAULT NULL,
  `cliente` varchar(255) DEFAULT NULL,
  `qtde_vendido` varchar(255) DEFAULT NULL,
  `total_venda` varchar(255) DEFAULT NULL,
  `horario_venda` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `monitoramento_vendas`
--

INSERT INTO `monitoramento_vendas` (`vendedor`, `cliente`, `qtde_vendido`, `total_venda`, `horario_venda`) VALUES
('Geovani Debastiani', '165.444.456-44', '2', '79900', '26/02/2022 / 13:29:08'),
('Geovani Debastiani', '129.107.059-19', '6', '2100', '28/02/2022 / 11:46:16'),
('Marcos Antônio', '165.444.456-44', '6', '1050', '28/02/2022 / 11:47:33'),
('Geovani Debastiani', '165.444.456-44', '15', '5250', '17/04/2022 / 22:00:09');

-- --------------------------------------------------------

--
-- Estrutura da tabela `produtos`
--

DROP TABLE IF EXISTS `produtos`;
CREATE TABLE IF NOT EXISTS `produtos` (
  `cód_produto` varchar(255) DEFAULT NULL,
  `descrição` varchar(255) DEFAULT NULL,
  `valor_unitário` varchar(255) DEFAULT NULL,
  `qtde_estoque` varchar(255) DEFAULT NULL,
  `fornecedor` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `produtos`
--

INSERT INTO `produtos` (`cód_produto`, `descrição`, `valor_unitário`, `qtde_estoque`, `fornecedor`) VALUES
('001', 'Leite 1l Tirol', '350', '14973', 'Tirol');

-- --------------------------------------------------------

--
-- Estrutura da tabela `quem_vendeu_mais`
--

DROP TABLE IF EXISTS `quem_vendeu_mais`;
CREATE TABLE IF NOT EXISTS `quem_vendeu_mais` (
  `nome` varchar(255) DEFAULT NULL,
  `total_qtde` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `quem_vendeu_mais`
--

INSERT INTO `quem_vendeu_mais` (`nome`, `total_qtde`) VALUES
('Geovani Debastiani', '23'),
('Marcos Antônio', '6');

-- --------------------------------------------------------

--
-- Estrutura da tabela `vendas`
--

DROP TABLE IF EXISTS `vendas`;
CREATE TABLE IF NOT EXISTS `vendas` (
  `cód` varchar(255) DEFAULT NULL,
  `produto` varchar(255) DEFAULT NULL,
  `valor_unitário` varchar(255) DEFAULT NULL,
  `qtde` varchar(255) DEFAULT NULL,
  `total` varchar(255) DEFAULT NULL,
  `id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
