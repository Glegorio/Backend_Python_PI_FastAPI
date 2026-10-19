-- Script DDL de criação do Banco de Dados MySQL
-- Sistema de Gestão para ONG de Futebol

CREATE DATABASE IF NOT EXISTS `ong_futebol` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `ong_futebol`;

-- 1. Tabela de Assistidos (Alunos)
CREATE TABLE IF NOT EXISTS `assistidos` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nome_completo` VARCHAR(150) NOT NULL,
    `data_nascimento` DATE NOT NULL,
    `cpf` VARCHAR(14) UNIQUE NULL,
    `nome_responsavel` VARCHAR(150) NOT NULL,
    `telefone_responsavel` VARCHAR(20) NOT NULL,
    `posicao_campo` VARCHAR(50) DEFAULT 'Indefinido',
    `ativo` TINYINT(1) DEFAULT 1,
    `criado_em` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `atualizado_em` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Tabela de Voluntários (Treinadores, Apoiadores, Staff)
CREATE TABLE IF NOT EXISTS `voluntarios` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nome_completo` VARCHAR(150) NOT NULL,
    `email` VARCHAR(150) UNIQUE NOT NULL,
    `telefone` VARCHAR(20) NOT NULL,
    `funcao` VARCHAR(80) NOT NULL, -- ex: Treinador, Preparador Físico, Monitor
    `ativo` TINYINT(1) DEFAULT 1,
    `criado_em` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `atualizado_em` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Tabela de Aulas / Treinos
CREATE TABLE IF NOT EXISTS `aulas` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `titulo` VARCHAR(100) NOT NULL, -- ex: Treino Sub-13 Tático
    `descricao` TEXT NULL,
    `data_hora` DATETIME NOT NULL,
    `local` VARCHAR(150) NOT NULL, -- ex: Campo Principal, Quadra Coberta
    `voluntario_id` INT NOT NULL,
    `criado_em` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `atualizado_em` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_aulas_voluntario` FOREIGN KEY (`voluntario_id`) REFERENCES `voluntarios` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Tabela de Chamadas / Presença dos Assistidos nas Aulas
CREATE TABLE IF NOT EXISTS `chamadas` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `aula_id` INT NOT NULL,
    `assistido_id` INT NOT NULL,
    `presente` TINYINT(1) NOT NULL DEFAULT 0,
    `observacao` VARCHAR(255) NULL, -- ex: Ausência justificada, Atestado
    `registrado_em` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_chamadas_aula` FOREIGN KEY (`aula_id`) REFERENCES `aulas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_chamadas_assistido` FOREIGN KEY (`assistido_id`) REFERENCES `assistidos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `uk_aula_assistido` UNIQUE (`aula_id`, `assistido_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Índices de Performance
CREATE INDEX `idx_assistidos_nome` ON `assistidos` (`nome_completo`);
CREATE INDEX `idx_aulas_data` ON `aulas` (`data_hora`);
CREATE INDEX `idx_chamadas_presente` ON `chamadas` (`presente`);