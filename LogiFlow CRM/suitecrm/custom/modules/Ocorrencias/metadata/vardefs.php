<?php
/**
 * LogiFlow CRM - Módulo Ocorrências
 * Vardefs - Definição de campos
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

$dictionary['Ocorrencias'] = array(
    'table' => 'ocorrencias',
    'audited' => true,
    'unified_search' => true,
    'comment' => 'Registro de ocorrências operacionais',
    
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
            'id_name' => 'assigned_user_id',
            'module' => 'Users',
            'rname' => 'user_name',
        ),
        
        // ========================================
        // CAMPOS ESPECÍFICOS DE OCORRÊNCIA
        // ========================================
        
        'numero_ocorrencia' => array(
            'name' => 'numero_ocorrencia',
            'vname' => 'LBL_NUMERO_OCORRENCIA',
            'type' => 'varchar',
            'len' => 20,
            'unified_search' => true,
        ),
        
        // Relacionamento com Pedido
        'pedido_id' => array(
            'name' => 'pedido_id',
            'vname' => 'LBL_PEDIDO_ID',
            'type' => 'id',
            'required' => true,
        ),
        'pedido_name' => array(
            'name' => 'pedido_name',
            'vname' => 'LBL_PEDIDO',
            'type' => 'relate',
            'source' => 'non-db',
            'id_name' => 'pedido_id',
            'module' => 'PedidosFrete',
            'link' => 'pedido_link',
            'rname' => 'name',
            'required' => true,
        ),
        
        // Tipo e Categoria
        'tipo' => array(
            'name' => 'tipo',
            'vname' => 'LBL_TIPO',
            'type' => 'enum',
            'options' => 'ocorrencia_tipo_list',
            'len' => 30,
            'required' => true,
        ),
        'categoria' => array(
            'name' => 'categoria',
            'vname' => 'LBL_CATEGORIA',
            'type' => 'enum',
            'options' => 'ocorrencia_categoria_list',
            'len' => 30,
        ),
        'gravidade' => array(
            'name' => 'gravidade',
            'vname' => 'LBL_GRAVIDADE',
            'type' => 'enum',
            'options' => 'ocorrencia_gravidade_list',
            'len' => 15,
            'default' => 'media',
            'required' => true,
        ),
        
        // Status
        'status' => array(
            'name' => 'status',
            'vname' => 'LBL_STATUS',
            'type' => 'enum',
            'options' => 'ocorrencia_status_list',
            'len' => 20,
            'default' => 'aberta',
            'required' => true,
            'audited' => true,
        ),
        
        // Datas
        'data_ocorrencia' => array(
            'name' => 'data_ocorrencia',
            'vname' => 'LBL_DATA_OCORRENCIA',
            'type' => 'datetimecombo',
            'dbType' => 'datetime',
            'required' => true,
        ),
        'data_resolucao' => array(
            'name' => 'data_resolucao',
            'vname' => 'LBL_DATA_RESOLUCAO',
            'type' => 'datetimecombo',
            'dbType' => 'datetime',
        ),
        
        // Localização
        'local' => array(
            'name' => 'local',
            'vname' => 'LBL_LOCAL',
            'type' => 'varchar',
            'len' => 255,
        ),
        'latitude' => array(
            'name' => 'latitude',
            'vname' => 'LBL_LATITUDE',
            'type' => 'decimal',
            'len' => '10',
            'precision' => '7',
        ),
        'longitude' => array(
            'name' => 'longitude',
            'vname' => 'LBL_LONGITUDE',
            'type' => 'decimal',
            'len' => '10',
            'precision' => '7',
        ),
        
        // Detalhes
        'descricao_detalhada' => array(
            'name' => 'descricao_detalhada',
            'vname' => 'LBL_DESCRICAO_DETALHADA',
            'type' => 'text',
            'required' => true,
        ),
        'acao_tomada' => array(
            'name' => 'acao_tomada',
            'vname' => 'LBL_ACAO_TOMADA',
            'type' => 'text',
        ),
        'resolucao' => array(
            'name' => 'resolucao',
            'vname' => 'LBL_RESOLUCAO',
            'type' => 'text',
        ),
        
        // Valores (para avarias, sinistros)
        'valor_prejuizo' => array(
            'name' => 'valor_prejuizo',
            'vname' => 'LBL_VALOR_PREJUIZO',
            'type' => 'currency',
            'len' => '26',
            'precision' => '2',
        ),
        'valor_ressarcimento' => array(
            'name' => 'valor_ressarcimento',
            'vname' => 'LBL_VALOR_RESSARCIMENTO',
            'type' => 'currency',
            'len' => '26',
            'precision' => '2',
        ),
        
        // Responsável
        'responsavel_id' => array(
            'name' => 'responsavel_id',
            'vname' => 'LBL_RESPONSAVEL_ID',
            'type' => 'id',
        ),
        'responsavel_name' => array(
            'name' => 'responsavel_name',
            'vname' => 'LBL_RESPONSAVEL',
            'type' => 'relate',
            'source' => 'non-db',
            'id_name' => 'responsavel_id',
            'module' => 'Users',
            'rname' => 'user_name',
        ),
        
        // Fotos/Documentos
        'foto_1' => array(
            'name' => 'foto_1',
            'vname' => 'LBL_FOTO_1',
            'type' => 'image',
            'dbType' => 'varchar',
            'len' => 255,
        ),
        'foto_2' => array(
            'name' => 'foto_2',
            'vname' => 'LBL_FOTO_2',
            'type' => 'image',
            'dbType' => 'varchar',
            'len' => 255,
        ),
        'foto_3' => array(
            'name' => 'foto_3',
            'vname' => 'LBL_FOTO_3',
            'type' => 'image',
            'dbType' => 'varchar',
            'len' => 255,
        ),
        
        // Boletim de ocorrência
        'bo_numero' => array(
            'name' => 'bo_numero',
            'vname' => 'LBL_BO_NUMERO',
            'type' => 'varchar',
            'len' => 30,
        ),
        'bo_delegacia' => array(
            'name' => 'bo_delegacia',
            'vname' => 'LBL_BO_DELEGACIA',
            'type' => 'varchar',
            'len' => 150,
        ),
        
        // Links
        'pedido_link' => array(
            'name' => 'pedido_link',
            'type' => 'link',
            'relationship' => 'pedidos_ocorrencias',
            'source' => 'non-db',
            'module' => 'PedidosFrete',
            'vname' => 'LBL_PEDIDO',
        ),
        'assigned_user_link' => array(
            'name' => 'assigned_user_link',
            'type' => 'link',
            'relationship' => 'ocorrencias_assigned_user',
            'source' => 'non-db',
            'module' => 'Users',
            'vname' => 'LBL_ASSIGNED_TO_USER',
        ),
    ),
    
    'relationships' => array(
        'pedidos_ocorrencias' => array(
            'lhs_module' => 'PedidosFrete',
            'lhs_table' => 'pedidos_frete',
            'lhs_key' => 'id',
            'rhs_module' => 'Ocorrencias',
            'rhs_table' => 'ocorrencias',
            'rhs_key' => 'pedido_id',
            'relationship_type' => 'one-to-many',
        ),
        'ocorrencias_assigned_user' => array(
            'lhs_module' => 'Users',
            'lhs_table' => 'users',
            'lhs_key' => 'id',
            'rhs_module' => 'Ocorrencias',
            'rhs_table' => 'ocorrencias',
            'rhs_key' => 'assigned_user_id',
            'relationship_type' => 'one-to-many',
        ),
    ),
    
    'indices' => array(
        array(
            'name' => 'idx_ocorrencias_numero',
            'type' => 'index',
            'fields' => array('numero_ocorrencia'),
        ),
        array(
            'name' => 'idx_ocorrencias_pedido',
            'type' => 'index',
            'fields' => array('pedido_id'),
        ),
        array(
            'name' => 'idx_ocorrencias_tipo',
            'type' => 'index',
            'fields' => array('tipo'),
        ),
        array(
            'name' => 'idx_ocorrencias_status',
            'type' => 'index',
            'fields' => array('status'),
        ),
        array(
            'name' => 'idx_ocorrencias_data',
            'type' => 'index',
            'fields' => array('data_ocorrencia'),
        ),
    ),
    
    'optimistic_locking' => true,
);

VardefManager::createVardef('Ocorrencias', 'Ocorrencias', array('basic', 'assignable', 'security_groups'));
