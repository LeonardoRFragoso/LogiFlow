<?php
/**
 * LogiFlow CRM - Módulo Pedidos de Frete
 * Vardefs - Definição de campos
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

$dictionary['PedidosFrete'] = array(
    'table' => 'pedidos_frete',
    'audited' => true,
    'unified_search' => true,
    'full_text_search' => true,
    'comment' => 'Pedidos de frete confirmados',
    
    'fields' => array(
        // Campos padrão
        'id' => array(
            'name' => 'id',
            'vname' => 'LBL_ID',
            'type' => 'id',
            'required' => true,
        ),
        'name' => array(
            'name' => 'name',
            'vname' => 'LBL_NAME',
            'type' => 'name',
            'dbType' => 'varchar',
            'len' => 255,
            'unified_search' => true,
            'required' => true,
        ),
        'date_entered' => array(
            'name' => 'date_entered',
            'vname' => 'LBL_DATE_ENTERED',
            'type' => 'datetime',
        ),
        'date_modified' => array(
            'name' => 'date_modified',
            'vname' => 'LBL_DATE_MODIFIED',
            'type' => 'datetime',
        ),
        'modified_user_id' => array(
            'name' => 'modified_user_id',
            'vname' => 'LBL_MODIFIED_USER_ID',
            'type' => 'id',
        ),
        'created_by' => array(
            'name' => 'created_by',
            'vname' => 'LBL_CREATED_BY',
            'type' => 'id',
        ),
        'description' => array(
            'name' => 'description',
            'vname' => 'LBL_DESCRIPTION',
            'type' => 'text',
        ),
        'deleted' => array(
            'name' => 'deleted',
            'vname' => 'LBL_DELETED',
            'type' => 'bool',
            'default' => '0',
        ),
        'assigned_user_id' => array(
            'name' => 'assigned_user_id',
            'vname' => 'LBL_ASSIGNED_TO_ID',
            'type' => 'id',
        ),
        'assigned_user_name' => array(
            'name' => 'assigned_user_name',
            'vname' => 'LBL_ASSIGNED_TO_NAME',
            'type' => 'relate',
            'source' => 'non-db',
            'table' => 'users',
            'id_name' => 'assigned_user_id',
            'module' => 'Users',
            'link' => 'assigned_user_link',
            'rname' => 'user_name',
        ),
        
        // ========================================
        // CAMPOS ESPECÍFICOS DE PEDIDO DE FRETE
        // ========================================
        
        'numero_pedido' => array(
            'name' => 'numero_pedido',
            'vname' => 'LBL_NUMERO_PEDIDO',
            'type' => 'varchar',
            'len' => 20,
            'unified_search' => true,
            'required' => true,
        ),
        'data_pedido' => array(
            'name' => 'data_pedido',
            'vname' => 'LBL_DATA_PEDIDO',
            'type' => 'date',
            'required' => true,
        ),
        
        // Relacionamento com Cotação
        'cotacao_id' => array(
            'name' => 'cotacao_id',
            'vname' => 'LBL_COTACAO_ID',
            'type' => 'id',
        ),
        'cotacao_name' => array(
            'name' => 'cotacao_name',
            'vname' => 'LBL_COTACAO',
            'type' => 'relate',
            'source' => 'non-db',
            'id_name' => 'cotacao_id',
            'module' => 'Cotacoes',
            'link' => 'cotacao_link',
            'rname' => 'name',
        ),
        
        // Relacionamento com Cliente
        'cliente_id' => array(
            'name' => 'cliente_id',
            'vname' => 'LBL_CLIENTE_ID',
            'type' => 'id',
            'required' => true,
        ),
        'cliente_name' => array(
            'name' => 'cliente_name',
            'vname' => 'LBL_CLIENTE',
            'type' => 'relate',
            'source' => 'non-db',
            'id_name' => 'cliente_id',
            'module' => 'Accounts',
            'link' => 'cliente_link',
            'rname' => 'name',
            'required' => true,
        ),
        
        // Origem
        'origem_cep' => array(
            'name' => 'origem_cep',
            'vname' => 'LBL_ORIGEM_CEP',
            'type' => 'varchar',
            'len' => 10,
        ),
        'origem_endereco' => array(
            'name' => 'origem_endereco',
            'vname' => 'LBL_ORIGEM_ENDERECO',
            'type' => 'varchar',
            'len' => 255,
            'required' => true,
        ),
        'origem_cidade' => array(
            'name' => 'origem_cidade',
            'vname' => 'LBL_ORIGEM_CIDADE',
            'type' => 'varchar',
            'len' => 100,
            'required' => true,
        ),
        'origem_uf' => array(
            'name' => 'origem_uf',
            'vname' => 'LBL_ORIGEM_UF',
            'type' => 'varchar',
            'len' => 2,
            'required' => true,
        ),
        'remetente_nome' => array(
            'name' => 'remetente_nome',
            'vname' => 'LBL_REMETENTE_NOME',
            'type' => 'varchar',
            'len' => 200,
        ),
        'remetente_telefone' => array(
            'name' => 'remetente_telefone',
            'vname' => 'LBL_REMETENTE_TELEFONE',
            'type' => 'phone',
            'len' => 20,
        ),
        
        // Destino
        'destino_cep' => array(
            'name' => 'destino_cep',
            'vname' => 'LBL_DESTINO_CEP',
            'type' => 'varchar',
            'len' => 10,
        ),
        'destino_endereco' => array(
            'name' => 'destino_endereco',
            'vname' => 'LBL_DESTINO_ENDERECO',
            'type' => 'varchar',
            'len' => 255,
            'required' => true,
        ),
        'destino_cidade' => array(
            'name' => 'destino_cidade',
            'vname' => 'LBL_DESTINO_CIDADE',
            'type' => 'varchar',
            'len' => 100,
            'required' => true,
        ),
        'destino_uf' => array(
            'name' => 'destino_uf',
            'vname' => 'LBL_DESTINO_UF',
            'type' => 'varchar',
            'len' => 2,
            'required' => true,
        ),
        'destinatario_nome' => array(
            'name' => 'destinatario_nome',
            'vname' => 'LBL_DESTINATARIO_NOME',
            'type' => 'varchar',
            'len' => 200,
            'required' => true,
        ),
        'destinatario_telefone' => array(
            'name' => 'destinatario_telefone',
            'vname' => 'LBL_DESTINATARIO_TELEFONE',
            'type' => 'phone',
            'len' => 20,
        ),
        'destinatario_documento' => array(
            'name' => 'destinatario_documento',
            'vname' => 'LBL_DESTINATARIO_DOCUMENTO',
            'type' => 'varchar',
            'len' => 18,
        ),
        
        // Carga
        'tipo_carga' => array(
            'name' => 'tipo_carga',
            'vname' => 'LBL_TIPO_CARGA',
            'type' => 'enum',
            'options' => 'tipo_carga_list',
            'len' => 50,
            'required' => true,
        ),
        'peso_kg' => array(
            'name' => 'peso_kg',
            'vname' => 'LBL_PESO_KG',
            'type' => 'decimal',
            'len' => '10',
            'precision' => '2',
            'required' => true,
        ),
        'cubagem_m3' => array(
            'name' => 'cubagem_m3',
            'vname' => 'LBL_CUBAGEM_M3',
            'type' => 'decimal',
            'len' => '10',
            'precision' => '3',
        ),
        'quantidade_volumes' => array(
            'name' => 'quantidade_volumes',
            'vname' => 'LBL_QUANTIDADE_VOLUMES',
            'type' => 'int',
            'len' => 6,
            'default' => 1,
        ),
        'valor_mercadoria' => array(
            'name' => 'valor_mercadoria',
            'vname' => 'LBL_VALOR_MERCADORIA',
            'type' => 'currency',
            'len' => '26',
            'precision' => '2',
        ),
        'descricao_carga' => array(
            'name' => 'descricao_carga',
            'vname' => 'LBL_DESCRICAO_CARGA',
            'type' => 'text',
        ),
        
        // Valores
        'valor_frete' => array(
            'name' => 'valor_frete',
            'vname' => 'LBL_VALOR_FRETE',
            'type' => 'currency',
            'len' => '26',
            'precision' => '2',
            'required' => true,
        ),
        'valor_seguro' => array(
            'name' => 'valor_seguro',
            'vname' => 'LBL_VALOR_SEGURO',
            'type' => 'currency',
            'len' => '26',
            'precision' => '2',
            'default' => '0.00',
        ),
        'valor_adicional' => array(
            'name' => 'valor_adicional',
            'vname' => 'LBL_VALOR_ADICIONAL',
            'type' => 'currency',
            'len' => '26',
            'precision' => '2',
            'default' => '0.00',
        ),
        'custo_estimado' => array(
            'name' => 'custo_estimado',
            'vname' => 'LBL_CUSTO_ESTIMADO',
            'type' => 'currency',
            'len' => '26',
            'precision' => '2',
        ),
        
        // Motorista e Veículo
        'motorista_id' => array(
            'name' => 'motorista_id',
            'vname' => 'LBL_MOTORISTA_ID',
            'type' => 'id',
        ),
        'motorista_name' => array(
            'name' => 'motorista_name',
            'vname' => 'LBL_MOTORISTA',
            'type' => 'relate',
            'source' => 'non-db',
            'id_name' => 'motorista_id',
            'module' => 'Motoristas',
            'link' => 'motorista_link',
            'rname' => 'name',
        ),
        'veiculo_id' => array(
            'name' => 'veiculo_id',
            'vname' => 'LBL_VEICULO_ID',
            'type' => 'id',
        ),
        'veiculo_name' => array(
            'name' => 'veiculo_name',
            'vname' => 'LBL_VEICULO',
            'type' => 'relate',
            'source' => 'non-db',
            'id_name' => 'veiculo_id',
            'module' => 'Veiculos',
            'link' => 'veiculo_link',
            'rname' => 'name',
        ),
        
        // Datas operacionais
        'previsao_coleta' => array(
            'name' => 'previsao_coleta',
            'vname' => 'LBL_PREVISAO_COLETA',
            'type' => 'datetimecombo',
            'dbType' => 'datetime',
        ),
        'data_coleta' => array(
            'name' => 'data_coleta',
            'vname' => 'LBL_DATA_COLETA',
            'type' => 'datetimecombo',
            'dbType' => 'datetime',
        ),
        'previsao_entrega' => array(
            'name' => 'previsao_entrega',
            'vname' => 'LBL_PREVISAO_ENTREGA',
            'type' => 'date',
            'required' => true,
        ),
        'data_entrega' => array(
            'name' => 'data_entrega',
            'vname' => 'LBL_DATA_ENTREGA',
            'type' => 'datetimecombo',
            'dbType' => 'datetime',
        ),
        
        // Status
        'status' => array(
            'name' => 'status',
            'vname' => 'LBL_STATUS',
            'type' => 'enum',
            'options' => 'pedido_status_list',
            'len' => 30,
            'default' => 'em_planejamento',
            'required' => true,
            'audited' => true,
        ),
        'sla_status' => array(
            'name' => 'sla_status',
            'vname' => 'LBL_SLA_STATUS',
            'type' => 'enum',
            'options' => 'sla_status_list',
            'len' => 15,
            'default' => 'verde',
        ),
        
        // CT-e
        'cte_numero' => array(
            'name' => 'cte_numero',
            'vname' => 'LBL_CTE_NUMERO',
            'type' => 'varchar',
            'len' => 20,
        ),
        'cte_chave' => array(
            'name' => 'cte_chave',
            'vname' => 'LBL_CTE_CHAVE',
            'type' => 'varchar',
            'len' => 44,
        ),
        'cte_status' => array(
            'name' => 'cte_status',
            'vname' => 'LBL_CTE_STATUS',
            'type' => 'enum',
            'options' => 'cte_status_list',
            'len' => 20,
        ),
        'cte_data_emissao' => array(
            'name' => 'cte_data_emissao',
            'vname' => 'LBL_CTE_DATA_EMISSAO',
            'type' => 'datetime',
        ),
        
        // MDF-e
        'mdfe_numero' => array(
            'name' => 'mdfe_numero',
            'vname' => 'LBL_MDFE_NUMERO',
            'type' => 'varchar',
            'len' => 20,
        ),
        'mdfe_chave' => array(
            'name' => 'mdfe_chave',
            'vname' => 'LBL_MDFE_CHAVE',
            'type' => 'varchar',
            'len' => 44,
        ),
        
        'observacoes' => array(
            'name' => 'observacoes',
            'vname' => 'LBL_OBSERVACOES',
            'type' => 'text',
        ),
        
        // Links de relacionamento
        'cotacao_link' => array(
            'name' => 'cotacao_link',
            'type' => 'link',
            'relationship' => 'cotacoes_pedidos',
            'source' => 'non-db',
            'module' => 'Cotacoes',
            'vname' => 'LBL_COTACAO',
        ),
        'cliente_link' => array(
            'name' => 'cliente_link',
            'type' => 'link',
            'relationship' => 'accounts_pedidos',
            'source' => 'non-db',
            'module' => 'Accounts',
            'vname' => 'LBL_CLIENTE',
        ),
        'motorista_link' => array(
            'name' => 'motorista_link',
            'type' => 'link',
            'relationship' => 'motoristas_pedidos',
            'source' => 'non-db',
            'module' => 'Motoristas',
            'vname' => 'LBL_MOTORISTA',
        ),
        'veiculo_link' => array(
            'name' => 'veiculo_link',
            'type' => 'link',
            'relationship' => 'veiculos_pedidos',
            'source' => 'non-db',
            'module' => 'Veiculos',
            'vname' => 'LBL_VEICULO',
        ),
        'entregas_link' => array(
            'name' => 'entregas_link',
            'type' => 'link',
            'relationship' => 'pedidos_entregas',
            'source' => 'non-db',
            'module' => 'Entregas',
            'vname' => 'LBL_ENTREGAS',
        ),
        'ocorrencias_link' => array(
            'name' => 'ocorrencias_link',
            'type' => 'link',
            'relationship' => 'pedidos_ocorrencias',
            'source' => 'non-db',
            'module' => 'Ocorrencias',
            'vname' => 'LBL_OCORRENCIAS',
        ),
        'assigned_user_link' => array(
            'name' => 'assigned_user_link',
            'type' => 'link',
            'relationship' => 'pedidos_assigned_user',
            'source' => 'non-db',
            'module' => 'Users',
            'vname' => 'LBL_ASSIGNED_TO_USER',
        ),
    ),
    
    'relationships' => array(
        'pedidos_assigned_user' => array(
            'lhs_module' => 'Users',
            'lhs_table' => 'users',
            'lhs_key' => 'id',
            'rhs_module' => 'PedidosFrete',
            'rhs_table' => 'pedidos_frete',
            'rhs_key' => 'assigned_user_id',
            'relationship_type' => 'one-to-many',
        ),
    ),
    
    'indices' => array(
        array(
            'name' => 'idx_pedidos_numero',
            'type' => 'unique',
            'fields' => array('numero_pedido'),
        ),
        array(
            'name' => 'idx_pedidos_cliente',
            'type' => 'index',
            'fields' => array('cliente_id'),
        ),
        array(
            'name' => 'idx_pedidos_cotacao',
            'type' => 'index',
            'fields' => array('cotacao_id'),
        ),
        array(
            'name' => 'idx_pedidos_motorista',
            'type' => 'index',
            'fields' => array('motorista_id'),
        ),
        array(
            'name' => 'idx_pedidos_status',
            'type' => 'index',
            'fields' => array('status'),
        ),
        array(
            'name' => 'idx_pedidos_sla',
            'type' => 'index',
            'fields' => array('sla_status'),
        ),
        array(
            'name' => 'idx_pedidos_previsao',
            'type' => 'index',
            'fields' => array('previsao_entrega'),
        ),
    ),
    
    'optimistic_locking' => true,
);

VardefManager::createVardef('PedidosFrete', 'PedidosFrete', array('basic', 'assignable', 'security_groups'));
