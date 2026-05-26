-- ============================================================================
-- LogiFlow CRM - Scripts SQL de Instalação
-- ============================================================================
-- Execute estes scripts no banco de dados do SuiteCRM após instalar os módulos
-- Versão: 1.0
-- Data: Dezembro 2025
-- ============================================================================

-- TABELA: pedidos_frete
CREATE TABLE IF NOT EXISTS `pedidos_frete` (
  `id` char(36) NOT NULL,
  `name` varchar(150) DEFAULT NULL,
  `date_entered` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `modified_user_id` char(36) DEFAULT NULL,
  `created_by` char(36) DEFAULT NULL,
  `description` text,
  `deleted` tinyint(1) DEFAULT '0',
  `assigned_user_id` char(36) DEFAULT NULL,
  
  -- Identificação
  `numero_pedido` varchar(50) NOT NULL,
  `data_pedido` date NOT NULL,
  `cotacao_id` char(36) DEFAULT NULL,
  `account_id` char(36) NOT NULL,
  `motorista_id` char(36) DEFAULT NULL,
  `veiculo_id` char(36) DEFAULT NULL,
  
  -- Origem
  `origem_cep` varchar(10) DEFAULT NULL,
  `origem_endereco` varchar(255) NOT NULL,
  `origem_cidade` varchar(100) NOT NULL,
  `origem_uf` varchar(2) NOT NULL,
  
  -- Destino
  `destino_cep` varchar(10) DEFAULT NULL,
  `destino_endereco` varchar(255) NOT NULL,
  `destino_cidade` varchar(100) NOT NULL,
  `destino_uf` varchar(2) NOT NULL,
  `destinatario_nome` varchar(150) DEFAULT NULL,
  `destinatario_telefone` varchar(20) DEFAULT NULL,
  
  -- Carga
  `tipo_carga` varchar(30) NOT NULL,
  `peso_kg` decimal(10,2) NOT NULL,
  `cubagem_m3` decimal(10,3) DEFAULT NULL,
  `quantidade_volumes` int(5) DEFAULT 1,
  `valor_mercadoria` decimal(12,2) DEFAULT NULL,
  
  -- Valores
  `valor_frete` decimal(12,2) NOT NULL,
  `valor_seguro` decimal(12,2) DEFAULT 0,
  `valor_adicional` decimal(12,2) DEFAULT 0,
  
  -- Datas
  `previsao_entrega` date NOT NULL,
  `data_entrega_real` datetime DEFAULT NULL,
  `data_coleta` datetime DEFAULT NULL,
  
  -- Status
  `status_operacional` varchar(30) DEFAULT 'em_planejamento',
  `sla_status` varchar(20) DEFAULT 'verde',
  
  -- CT-e
  `cte_numero` varchar(20) DEFAULT NULL,
  `cte_chave` varchar(44) DEFAULT NULL,
  `cte_status` varchar(20) DEFAULT 'pendente',
  `cte_data_emissao` datetime DEFAULT NULL,
  `cte_xml` text,
  `cte_pdf_url` varchar(255) DEFAULT NULL,
  
  -- MDF-e
  `mdfe_numero` varchar(20) DEFAULT NULL,
  `mdfe_chave` varchar(44) DEFAULT NULL,
  
  `observacoes` text,
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_pedidos_numero` (`numero_pedido`),
  KEY `idx_pedidos_account` (`account_id`),
  KEY `idx_pedidos_cotacao` (`cotacao_id`),
  KEY `idx_pedidos_motorista` (`motorista_id`),
  KEY `idx_pedidos_veiculo` (`veiculo_id`),
  KEY `idx_pedidos_status` (`status_operacional`),
  KEY `idx_pedidos_sla` (`sla_status`),
  KEY `idx_pedidos_previsao` (`previsao_entrega`),
  KEY `idx_pedidos_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- TABELA: motoristas
CREATE TABLE IF NOT EXISTS `motoristas` (
  `id` char(36) NOT NULL,
  `name` varchar(150) NOT NULL COMMENT 'Nome completo',
  `date_entered` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `modified_user_id` char(36) DEFAULT NULL,
  `created_by` char(36) DEFAULT NULL,
  `description` text,
  `deleted` tinyint(1) DEFAULT '0',
  `assigned_user_id` char(36) DEFAULT NULL,
  
  -- Dados Pessoais
  `cpf` varchar(14) NOT NULL,
  `rg` varchar(20) DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  
  -- Contato
  `celular` varchar(20) NOT NULL,
  `telefone_emergencia` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  
  -- Endereço
  `endereco` varchar(255) DEFAULT NULL,
  `cidade` varchar(100) DEFAULT NULL,
  `uf` varchar(2) DEFAULT NULL,
  `cep` varchar(10) DEFAULT NULL,
  
  -- CNH
  `cnh` varchar(20) NOT NULL,
  `categoria_cnh` varchar(5) NOT NULL,
  `vencimento_cnh` date NOT NULL,
  `primeira_habilitacao` date DEFAULT NULL,
  
  -- Profissional
  `data_admissao` date DEFAULT NULL,
  `data_demissao` date DEFAULT NULL,
  `tipo_contrato` varchar(20) DEFAULT 'clt',
  `status` varchar(20) DEFAULT 'disponivel',
  
  -- App Mobile
  `usuario_app_id` char(36) DEFAULT NULL,
  
  -- Avaliação
  `avaliacao_media` decimal(3,2) DEFAULT 0,
  `total_entregas` int DEFAULT 0,
  `entregas_no_prazo` int DEFAULT 0,
  
  `foto_url` varchar(255) DEFAULT NULL,
  `observacoes` text,
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_motoristas_cpf` (`cpf`),
  UNIQUE KEY `idx_motoristas_cnh` (`cnh`),
  KEY `idx_motoristas_status` (`status`),
  KEY `idx_motoristas_vencimento_cnh` (`vencimento_cnh`),
  KEY `idx_motoristas_usuario_app` (`usuario_app_id`),
  KEY `idx_motoristas_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- TABELA: veiculos
CREATE TABLE IF NOT EXISTS `veiculos` (
  `id` char(36) NOT NULL,
  `name` varchar(150) NOT NULL COMMENT 'Identificação do veículo',
  `date_entered` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `modified_user_id` char(36) DEFAULT NULL,
  `created_by` char(36) DEFAULT NULL,
  `description` text,
  `deleted` tinyint(1) DEFAULT '0',
  `assigned_user_id` char(36) DEFAULT NULL,
  
  -- Identificação
  `placa` varchar(8) NOT NULL,
  `renavam` varchar(15) DEFAULT NULL,
  `chassi` varchar(20) DEFAULT NULL,
  
  -- Especificações
  `tipo_veiculo` varchar(30) NOT NULL,
  `marca` varchar(50) DEFAULT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `ano_fabricacao` int(4) DEFAULT NULL,
  `ano_modelo` int(4) DEFAULT NULL,
  `cor` varchar(30) DEFAULT NULL,
  
  -- Capacidade
  `capacidade_kg` decimal(10,2) DEFAULT NULL,
  `capacidade_m3` decimal(10,2) DEFAULT NULL,
  `numero_eixos` int(2) DEFAULT NULL,
  
  -- Propriedade
  `tipo_propriedade` varchar(20) DEFAULT 'proprio',
  `valor_compra` decimal(12,2) DEFAULT NULL,
  `data_aquisicao` date DEFAULT NULL,
  
  -- Documentação
  `vencimento_licenciamento` date DEFAULT NULL,
  `vencimento_seguro` date DEFAULT NULL,
  `numero_apolice` varchar(50) DEFAULT NULL,
  `seguradora` varchar(100) DEFAULT NULL,
  
  -- Manutenção
  `ultima_manutencao` date DEFAULT NULL,
  `proxima_manutencao` date DEFAULT NULL,
  `km_atual` int(10) DEFAULT NULL,
  `km_proxima_manutencao` int(10) DEFAULT NULL,
  `tipo_ultima_manutencao` varchar(30) DEFAULT NULL,
  `custo_ultima_manutencao` decimal(12,2) DEFAULT NULL,
  
  -- Status
  `status` varchar(20) DEFAULT 'disponivel',
  `status_manutencao` varchar(20) DEFAULT 'ok',
  
  -- Relacionamento
  `motorista_padrao_id` char(36) DEFAULT NULL,
  
  -- Rastreamento
  `tem_rastreador` tinyint(1) DEFAULT 0,
  `rastreador_id` varchar(50) DEFAULT NULL,
  `rastreador_modelo` varchar(50) DEFAULT NULL,
  
  -- Estatísticas
  `total_viagens` int DEFAULT 0,
  `km_total` int(10) DEFAULT 0,
  
  `observacoes` text,
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_veiculos_placa` (`placa`),
  KEY `idx_veiculos_renavam` (`renavam`),
  KEY `idx_veiculos_status` (`status`),
  KEY `idx_veiculos_motorista` (`motorista_padrao_id`),
  KEY `idx_veiculos_licenciamento` (`vencimento_licenciamento`),
  KEY `idx_veiculos_manutencao` (`proxima_manutencao`),
  KEY `idx_veiculos_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- TABELA: entregas
CREATE TABLE IF NOT EXISTS `entregas` (
  `id` char(36) NOT NULL,
  `name` varchar(150) NOT NULL,
  `date_entered` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `modified_user_id` char(36) DEFAULT NULL,
  `created_by` char(36) DEFAULT NULL,
  `description` text,
  `deleted` tinyint(1) DEFAULT '0',
  `assigned_user_id` char(36) DEFAULT NULL,
  
  -- Relacionamento
  `pedido_id` char(36) NOT NULL,
  `numero_rastreio` varchar(50) DEFAULT NULL,
  
  -- Status e Localização
  `status` varchar(30) DEFAULT 'aguardando_coleta',
  `local_atual` varchar(255) DEFAULT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  
  -- Eventos
  `ultimo_evento` varchar(255) DEFAULT NULL,
  `data_ultimo_evento` datetime DEFAULT NULL,
  
  -- Datas
  `data_coleta` datetime DEFAULT NULL,
  `data_saida_entrega` datetime DEFAULT NULL,
  `data_entrega` datetime DEFAULT NULL,
  
  -- Comprovante
  `foto_comprovante` varchar(255) DEFAULT NULL,
  `assinatura` text,
  `nome_recebedor` varchar(150) DEFAULT NULL,
  `documento_recebedor` varchar(20) DEFAULT NULL,
  
  -- Tentativas
  `numero_tentativas` int(2) DEFAULT 0,
  `data_proxima_tentativa` datetime DEFAULT NULL,
  `motivo_nao_entrega` varchar(50) DEFAULT NULL,
  
  -- Avaliação
  `avaliacao_cliente` int(1) DEFAULT NULL COMMENT 'Nota 1-5',
  `comentario_cliente` text,
  
  -- Notificações
  `cliente_notificado` tinyint(1) DEFAULT 0,
  `data_notificacao` datetime DEFAULT NULL,
  
  `observacoes` text,
  `observacoes_motorista` text,
  
  PRIMARY KEY (`id`),
  KEY `idx_entregas_pedido` (`pedido_id`),
  KEY `idx_entregas_status` (`status`),
  KEY `idx_entregas_rastreio` (`numero_rastreio`),
  KEY `idx_entregas_data_entrega` (`data_entrega`),
  KEY `idx_entregas_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- TABELA: ocorrencias
CREATE TABLE IF NOT EXISTS `ocorrencias` (
  `id` char(36) NOT NULL,
  `name` varchar(150) NOT NULL,
  `date_entered` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `modified_user_id` char(36) DEFAULT NULL,
  `created_by` char(36) DEFAULT NULL,
  `description` text,
  `deleted` tinyint(1) DEFAULT '0',
  `assigned_user_id` char(36) DEFAULT NULL,
  
  -- Relacionamento
  `pedido_id` char(36) NOT NULL,
  
  -- Classificação
  `tipo_ocorrencia` varchar(30) NOT NULL,
  `gravidade` varchar(20) DEFAULT 'media',
  
  -- Detalhes
  `data_ocorrencia` datetime NOT NULL,
  `local_ocorrencia` varchar(255) DEFAULT NULL,
  `descricao_detalhada` text NOT NULL,
  
  -- Envolvidos
  `motorista_envolvido_id` char(36) DEFAULT NULL,
  `veiculo_envolvido_id` char(36) DEFAULT NULL,
  `responsavel_id` char(36) DEFAULT NULL,
  
  -- Financeiro
  `custo_estimado` decimal(12,2) DEFAULT NULL,
  `custo_real` decimal(12,2) DEFAULT NULL,
  `valor_recuperado` decimal(12,2) DEFAULT NULL,
  
  -- Status
  `status` varchar(30) DEFAULT 'aberta',
  `data_resolucao` datetime DEFAULT NULL,
  `solucao` text,
  
  -- Ações
  `acao_imediata` text,
  `acao_preventiva` text,
  
  -- Documentação
  `boletim_ocorrencia` varchar(50) DEFAULT NULL,
  `numero_sinistro` varchar(50) DEFAULT NULL,
  
  -- Notificação
  `cliente_notificado` tinyint(1) DEFAULT 0,
  `data_notificacao_cliente` datetime DEFAULT NULL,
  
  `observacoes` text,
  
  PRIMARY KEY (`id`),
  KEY `idx_ocorrencias_pedido` (`pedido_id`),
  KEY `idx_ocorrencias_tipo` (`tipo_ocorrencia`),
  KEY `idx_ocorrencias_gravidade` (`gravidade`),
  KEY `idx_ocorrencias_status` (`status`),
  KEY `idx_ocorrencias_data` (`data_ocorrencia`),
  KEY `idx_ocorrencias_motorista` (`motorista_envolvido_id`),
  KEY `idx_ocorrencias_veiculo` (`veiculo_envolvido_id`),
  KEY `idx_ocorrencias_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- RELACIONAMENTOS (Tabelas intermediárias se necessário)
-- ============================================================================
-- O SuiteCRM gerencia relacionamentos via vardefs, mas tabelas diretas também podem ser criadas

-- ============================================================================
-- DADOS INICIAIS (OPCIONAL)
-- ============================================================================

-- Inserir usuário admin padrão se necessário
-- INSERT INTO users (id, user_name, first_name, last_name, status) 
-- VALUES (UUID(), 'admin', 'Admin', 'LogiFlow', 'Active');

-- ============================================================================
-- FIM DOS SCRIPTS
-- ============================================================================
