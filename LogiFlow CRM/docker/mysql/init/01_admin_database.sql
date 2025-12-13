-- =============================================
-- LogiFlow CRM - Admin Database Initialization
-- =============================================
-- Este script cria a base administrativa para 
-- gerenciamento de tenants do SaaS

-- Criar banco administrativo
CREATE DATABASE IF NOT EXISTS `logiflow_admin` 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE `logiflow_admin`;

-- =============================================
-- Tabela de Tenants
-- =============================================
CREATE TABLE IF NOT EXISTS `tenants` (
    `id` VARCHAR(36) PRIMARY KEY,
    `slug` VARCHAR(100) NOT NULL UNIQUE,
    `name` VARCHAR(255) NOT NULL,
    `cnpj` VARCHAR(18) UNIQUE,
    `email` VARCHAR(255) NOT NULL,
    `phone` VARCHAR(20),
    
    -- Banco de dados
    `database_host` VARCHAR(255) DEFAULT 'db',
    `database_name` VARCHAR(100) NOT NULL,
    `database_user` VARCHAR(100) NOT NULL,
    
    -- Plano e Status
    `plan` ENUM('trial', 'start', 'pro', 'premium') DEFAULT 'trial',
    `status` ENUM('active', 'trial', 'suspended', 'cancelled') DEFAULT 'trial',
    `trial_ends_at` DATETIME,
    
    -- Limites do plano
    `max_users` INT DEFAULT 5,
    `storage_limit_mb` INT DEFAULT 1024,
    `storage_used_mb` DECIMAL(10,2) DEFAULT 0,
    
    -- Configurações
    `settings` JSON,
    `features` JSON,
    
    -- Billing
    `billing_customer_id` VARCHAR(100),
    `billing_subscription_id` VARCHAR(100),
    
    -- Timestamps
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `suspended_at` TIMESTAMP NULL,
    `cancelled_at` TIMESTAMP NULL,
    
    INDEX `idx_status` (`status`),
    INDEX `idx_plan` (`plan`),
    INDEX `idx_slug` (`slug`)
) ENGINE=InnoDB;

-- =============================================
-- Tabela de Usuários Admin
-- =============================================
CREATE TABLE IF NOT EXISTS `admin_users` (
    `id` VARCHAR(36) PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `role` ENUM('superadmin', 'admin', 'support') DEFAULT 'support',
    `is_active` BOOLEAN DEFAULT TRUE,
    `last_login` TIMESTAMP NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =============================================
-- Tabela de Planos
-- =============================================
CREATE TABLE IF NOT EXISTS `plans` (
    `id` VARCHAR(36) PRIMARY KEY,
    `code` VARCHAR(50) NOT NULL UNIQUE,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `price_monthly` DECIMAL(10,2) NOT NULL,
    `price_yearly` DECIMAL(10,2),
    `max_users` INT NOT NULL,
    `storage_mb` INT NOT NULL,
    `features` JSON,
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Inserir planos padrão
INSERT INTO `plans` (`id`, `code`, `name`, `description`, `price_monthly`, `price_yearly`, `max_users`, `storage_mb`, `features`) VALUES
(UUID(), 'trial', 'Trial', 'Período de teste gratuito por 14 dias', 0, 0, 3, 512, '{"cotacoes": true, "pedidos": true, "entregas": true, "cte": false, "whatsapp": false, "api": false}'),
(UUID(), 'start', 'Start', 'Para pequenas transportadoras', 299.00, 2990.00, 5, 2048, '{"cotacoes": true, "pedidos": true, "entregas": true, "motoristas": true, "veiculos": true, "cte": false, "whatsapp": false, "api": false}'),
(UUID(), 'pro', 'Pro', 'Para transportadoras em crescimento', 599.00, 5990.00, 15, 10240, '{"cotacoes": true, "pedidos": true, "entregas": true, "motoristas": true, "veiculos": true, "cte": true, "whatsapp": true, "api": true, "relatorios_avancados": true}'),
(UUID(), 'premium', 'Premium', 'Para grandes operações', 1499.00, 14990.00, 50, 51200, '{"cotacoes": true, "pedidos": true, "entregas": true, "motoristas": true, "veiculos": true, "cte": true, "whatsapp": true, "api": true, "relatorios_avancados": true, "integracao_erp": true, "suporte_prioritario": true}');

-- =============================================
-- Tabela de Logs de Atividade
-- =============================================
CREATE TABLE IF NOT EXISTS `activity_logs` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `tenant_id` VARCHAR(36),
    `user_id` VARCHAR(36),
    `action` VARCHAR(100) NOT NULL,
    `entity_type` VARCHAR(100),
    `entity_id` VARCHAR(36),
    `details` JSON,
    `ip_address` VARCHAR(45),
    `user_agent` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX `idx_tenant` (`tenant_id`),
    INDEX `idx_action` (`action`),
    INDEX `idx_created` (`created_at`),
    
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- =============================================
-- Tabela de Métricas de Uso
-- =============================================
CREATE TABLE IF NOT EXISTS `usage_metrics` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `tenant_id` VARCHAR(36) NOT NULL,
    `metric_date` DATE NOT NULL,
    `active_users` INT DEFAULT 0,
    `logins` INT DEFAULT 0,
    `cotacoes_criadas` INT DEFAULT 0,
    `pedidos_criados` INT DEFAULT 0,
    `entregas_concluidas` INT DEFAULT 0,
    `ctes_emitidos` INT DEFAULT 0,
    `api_calls` INT DEFAULT 0,
    `storage_used_mb` DECIMAL(10,2) DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY `uk_tenant_date` (`tenant_id`, `metric_date`),
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- =============================================
-- Tabela de Health Score
-- =============================================
CREATE TABLE IF NOT EXISTS `tenant_health_scores` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `tenant_id` VARCHAR(36) NOT NULL,
    `score_date` DATE NOT NULL,
    `total_score` INT NOT NULL,
    `usage_score` INT DEFAULT 0,
    `adoption_score` INT DEFAULT 0,
    `engagement_score` INT DEFAULT 0,
    `support_score` INT DEFAULT 0,
    `financial_score` INT DEFAULT 0,
    `classification` ENUM('healthy', 'attention', 'risk', 'critical') NOT NULL,
    `details` JSON,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY `uk_tenant_date` (`tenant_id`, `score_date`),
    INDEX `idx_classification` (`classification`),
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- =============================================
-- Inserir admin padrão (senha: admin123)
-- =============================================
INSERT INTO `admin_users` (`id`, `email`, `password_hash`, `name`, `role`) VALUES
(UUID(), 'admin@logiflow.com.br', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VLnPBqKmX9hKHu', 'Administrador', 'superadmin');

-- =============================================
-- Criar banco template para novos tenants
-- =============================================
CREATE DATABASE IF NOT EXISTS `logiflow_template`
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;
