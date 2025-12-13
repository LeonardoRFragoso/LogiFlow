<?php
/**
 * LogiFlow CRM - Módulo Cotações
 * Vardefs - Definição de campos
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

$dictionary['Cotacoes'] = array(
    'table' => 'cotacoes',
    'audited' => true,
    'unified_search' => true,
    'full_text_search' => true,
    'unified_search_default_enabled' => true,
    'duplicate_merge' => true,
    'comment' => 'Cotações de frete para clientes',
    
    'fields' => array(
        // Campos padrão herdados
        'id' => array(
            'name' => 'id',
            'vname' => 'LBL_ID',
            'type' => 'id',
            'required' => true,
            'reportable' => true,
        ),
        'name' => array(
            'name' => 'name',
            'vname' => 'LBL_NAME',
            'type' => 'name',
            'link' => true,
            'dbType' => 'varchar',
            'len' => 255,
            'unified_search' => true,
            'full_text_search' => array('boost' => 3),
            'required' => true,
            'importable' => 'required',
        ),
        'date_entered' => array(
            'name' => 'date_entered',
            'vname' => 'LBL_DATE_ENTERED',
            'type' => 'datetime',
            'group' => 'created_by_name',
            'enable_range_search' => true,
        ),
        'date_modified' => array(
            'name' => 'date_modified',
            'vname' => 'LBL_DATE_MODIFIED',
            'type' => 'datetime',
            'group' => 'modified_by_name',
            'enable_range_search' => true,
        ),
        'modified_user_id' => array(
            'name' => 'modified_user_id',
            'rname' => 'user_name',
            'id_name' => 'modified_user_id',
            'vname' => 'LBL_MODIFIED',
            'type' => 'assigned_user_name',
            'table' => 'users',
            'isnull' => 'false',
            'dbType' => 'id',
        ),
        'created_by' => array(
            'name' => 'created_by',
            'rname' => 'user_name',
            'id_name' => 'created_by',
            'vname' => 'LBL_CREATED',
            'type' => 'assigned_user_name',
            'table' => 'users',
            'isnull' => 'false',
            'dbType' => 'id',
        ),
        'description' => array(
            'name' => 'description',
            'vname' => 'LBL_DESCRIPTION',
            'type' => 'text',
            'rows' => 4,
            'cols' => 60,
        ),
        'deleted' => array(
            'name' => 'deleted',
            'vname' => 'LBL_DELETED',
            'type' => 'bool',
            'default' => '0',
            'reportable' => false,
        ),
        'assigned_user_id' => array(
            'name' => 'assigned_user_id',
            'rname' => 'user_name',
            'id_name' => 'assigned_user_id',
            'vname' => 'LBL_ASSIGNED_TO_ID',
            'type' => 'relate',
            'table' => 'users',
            'module' => 'Users',
            'reportable' => true,
            'isnull' => 'false',
            'dbType' => 'id',
        ),
        'assigned_user_name' => array(
            'name' => 'assigned_user_name',
            'link' => 'assigned_user_link',
            'vname' => 'LBL_ASSIGNED_TO_NAME',
            'rname' => 'user_name',
            'type' => 'relate',
            'reportable' => false,
            'source' => 'non-db',
            'table' => 'users',
            'id_name' => 'assigned_user_id',
            'module' => 'Users',
        ),
        
        // ========================================
        // CAMPOS ESPECÍFICOS DO MÓDULO COTAÇÕES
        // ========================================
        
        'numero_cotacao' => array(
            'name' => 'numero_cotacao',
            'vname' => 'LBL_NUMERO_COTACAO',
            'type' => 'varchar',
            'len' => 20,
            'unified_search' => true,
            'comment' => 'Número único da cotação',
            'importable' => true,
        ),
        
        // Relacionamento com Cliente (Accounts)
        'cliente_id' => array(
            'name' => 'cliente_id',
            'vname' => 'LBL_CLIENTE_ID',
            'type' => 'id',
            'reportable' => false,
        ),
        'cliente_name' => array(
            'name' => 'cliente_name',
            'rname' => 'name',
            'id_name' => 'cliente_id',
            'vname' => 'LBL_CLIENTE',
            'type' => 'relate',
            'link' => 'cliente_link',
            'table' => 'accounts',
            'isnull' => 'true',
            'module' => 'Accounts',
            'dbType' => 'varchar',
            'len' => 255,
            'source' => 'non-db',
            'unified_search' => true,
            'required' => true,
        ),
        
        // Origem e Destino
        'origem_cep' => array(
            'name' => 'origem_cep',
            'vname' => 'LBL_ORIGEM_CEP',
            'type' => 'varchar',
            'len' => 10,
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
        'origem_endereco' => array(
            'name' => 'origem_endereco',
            'vname' => 'LBL_ORIGEM_ENDERECO',
            'type' => 'varchar',
            'len' => 255,
        ),
        
        'destino_cep' => array(
            'name' => 'destino_cep',
            'vname' => 'LBL_DESTINO_CEP',
            'type' => 'varchar',
            'len' => 10,
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
        'destino_endereco' => array(
            'name' => 'destino_endereco',
            'vname' => 'LBL_DESTINO_ENDERECO',
            'type' => 'varchar',
            'len' => 255,
        ),
        
        // Características da Carga
        'tipo_carga' => array(
            'name' => 'tipo_carga',
            'vname' => 'LBL_TIPO_CARGA',
            'type' => 'enum',
            'options' => 'tipo_carga_list',
            'len' => 50,
            'default' => 'geral',
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
            'dbType' => 'decimal',
            'len' => '26',
            'precision' => '2',
        ),
        
        // Modal e Prazo
        'modal' => array(
            'name' => 'modal',
            'vname' => 'LBL_MODAL',
            'type' => 'enum',
            'options' => 'modal_transporte_list',
            'len' => 30,
            'default' => 'rodoviario',
            'required' => true,
        ),
        'prazo_estimado' => array(
            'name' => 'prazo_estimado',
            'vname' => 'LBL_PRAZO_ESTIMADO',
            'type' => 'int',
            'len' => 4,
            'comment' => 'Prazo em dias úteis',
            'required' => true,
        ),
        
        // Valores
        'valor_frete' => array(
            'name' => 'valor_frete',
            'vname' => 'LBL_VALOR_FRETE',
            'type' => 'currency',
            'dbType' => 'decimal',
            'len' => '26',
            'precision' => '2',
            'required' => true,
        ),
        'valor_seguro' => array(
            'name' => 'valor_seguro',
            'vname' => 'LBL_VALOR_SEGURO',
            'type' => 'currency',
            'dbType' => 'decimal',
            'len' => '26',
            'precision' => '2',
            'default' => '0.00',
        ),
        'valor_adicional' => array(
            'name' => 'valor_adicional',
            'vname' => 'LBL_VALOR_ADICIONAL',
            'type' => 'currency',
            'dbType' => 'decimal',
            'len' => '26',
            'precision' => '2',
            'default' => '0.00',
        ),
        'valor_total' => array(
            'name' => 'valor_total',
            'vname' => 'LBL_VALOR_TOTAL',
            'type' => 'currency',
            'dbType' => 'decimal',
            'len' => '26',
            'precision' => '2',
            'comment' => 'Valor total = frete + seguro + adicional',
        ),
        
        // Status e Validade
        'status' => array(
            'name' => 'status',
            'vname' => 'LBL_STATUS',
            'type' => 'enum',
            'options' => 'cotacao_status_list',
            'len' => 30,
            'default' => 'aberta',
            'required' => true,
            'audited' => true,
        ),
        'validade' => array(
            'name' => 'validade',
            'vname' => 'LBL_VALIDADE',
            'type' => 'date',
            'required' => true,
        ),
        'motivo_perda' => array(
            'name' => 'motivo_perda',
            'vname' => 'LBL_MOTIVO_PERDA',
            'type' => 'enum',
            'options' => 'motivo_perda_list',
            'len' => 50,
        ),
        'observacoes' => array(
            'name' => 'observacoes',
            'vname' => 'LBL_OBSERVACOES',
            'type' => 'text',
            'rows' => 4,
            'cols' => 60,
        ),
        
        // Contato do cliente
        'contato_nome' => array(
            'name' => 'contato_nome',
            'vname' => 'LBL_CONTATO_NOME',
            'type' => 'varchar',
            'len' => 150,
        ),
        'contato_telefone' => array(
            'name' => 'contato_telefone',
            'vname' => 'LBL_CONTATO_TELEFONE',
            'type' => 'phone',
            'dbType' => 'varchar',
            'len' => 20,
        ),
        'contato_email' => array(
            'name' => 'contato_email',
            'vname' => 'LBL_CONTATO_EMAIL',
            'type' => 'varchar',
            'len' => 255,
        ),
        
        // Relacionamentos
        'cliente_link' => array(
            'name' => 'cliente_link',
            'type' => 'link',
            'relationship' => 'accounts_cotacoes',
            'source' => 'non-db',
            'module' => 'Accounts',
            'bean_name' => 'Account',
            'vname' => 'LBL_CLIENTE',
        ),
        'pedidos_link' => array(
            'name' => 'pedidos_link',
            'type' => 'link',
            'relationship' => 'cotacoes_pedidos',
            'source' => 'non-db',
            'module' => 'PedidosFrete',
            'vname' => 'LBL_PEDIDOS',
        ),
        'assigned_user_link' => array(
            'name' => 'assigned_user_link',
            'type' => 'link',
            'relationship' => 'cotacoes_assigned_user',
            'vname' => 'LBL_ASSIGNED_TO_USER',
            'link_type' => 'one',
            'module' => 'Users',
            'bean_name' => 'User',
            'source' => 'non-db',
        ),
    ),
    
    'relationships' => array(
        'cotacoes_assigned_user' => array(
            'lhs_module' => 'Users',
            'lhs_table' => 'users',
            'lhs_key' => 'id',
            'rhs_module' => 'Cotacoes',
            'rhs_table' => 'cotacoes',
            'rhs_key' => 'assigned_user_id',
            'relationship_type' => 'one-to-many',
        ),
    ),
    
    'indices' => array(
        array(
            'name' => 'idx_cotacoes_numero',
            'type' => 'unique',
            'fields' => array('numero_cotacao'),
        ),
        array(
            'name' => 'idx_cotacoes_cliente',
            'type' => 'index',
            'fields' => array('cliente_id'),
        ),
        array(
            'name' => 'idx_cotacoes_status',
            'type' => 'index',
            'fields' => array('status'),
        ),
        array(
            'name' => 'idx_cotacoes_validade',
            'type' => 'index',
            'fields' => array('validade'),
        ),
    ),
    
    'optimistic_locking' => true,
);

VardefManager::createVardef('Cotacoes', 'Cotacoes', array('basic', 'assignable', 'security_groups'));
