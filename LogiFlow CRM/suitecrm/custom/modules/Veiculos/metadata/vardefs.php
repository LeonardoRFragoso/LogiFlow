<?php
/**
 * LogiFlow CRM - Módulo Veículos
 * Vardefs - Definição de campos
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

$dictionary['Veiculos'] = array(
    'table' => 'veiculos',
    'audited' => true,
    'unified_search' => true,
    'comment' => 'Cadastro de veículos da frota',
    
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
            'len' => 100,
            'unified_search' => true,
            'required' => true,
            'comment' => 'Identificação do veículo (Placa - Modelo)',
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
        
        // ========================================
        // CAMPOS ESPECÍFICOS DE VEÍCULO
        // ========================================
        
        // Identificação
        'placa' => array(
            'name' => 'placa',
            'vname' => 'LBL_PLACA',
            'type' => 'varchar',
            'len' => 10,
            'unified_search' => true,
            'required' => true,
        ),
        'renavam' => array(
            'name' => 'renavam',
            'vname' => 'LBL_RENAVAM',
            'type' => 'varchar',
            'len' => 15,
        ),
        'chassi' => array(
            'name' => 'chassi',
            'vname' => 'LBL_CHASSI',
            'type' => 'varchar',
            'len' => 20,
        ),
        
        // Características
        'tipo_veiculo' => array(
            'name' => 'tipo_veiculo',
            'vname' => 'LBL_TIPO_VEICULO',
            'type' => 'enum',
            'options' => 'tipo_veiculo_list',
            'len' => 30,
            'required' => true,
        ),
        'marca' => array(
            'name' => 'marca',
            'vname' => 'LBL_MARCA',
            'type' => 'varchar',
            'len' => 50,
        ),
        'modelo' => array(
            'name' => 'modelo',
            'vname' => 'LBL_MODELO',
            'type' => 'varchar',
            'len' => 100,
        ),
        'ano_fabricacao' => array(
            'name' => 'ano_fabricacao',
            'vname' => 'LBL_ANO_FABRICACAO',
            'type' => 'int',
            'len' => 4,
        ),
        'ano_modelo' => array(
            'name' => 'ano_modelo',
            'vname' => 'LBL_ANO_MODELO',
            'type' => 'int',
            'len' => 4,
        ),
        'cor' => array(
            'name' => 'cor',
            'vname' => 'LBL_COR',
            'type' => 'varchar',
            'len' => 30,
        ),
        'combustivel' => array(
            'name' => 'combustivel',
            'vname' => 'LBL_COMBUSTIVEL',
            'type' => 'enum',
            'options' => 'combustivel_list',
            'len' => 20,
        ),
        
        // Capacidade
        'capacidade_kg' => array(
            'name' => 'capacidade_kg',
            'vname' => 'LBL_CAPACIDADE_KG',
            'type' => 'decimal',
            'len' => '10',
            'precision' => '2',
        ),
        'capacidade_m3' => array(
            'name' => 'capacidade_m3',
            'vname' => 'LBL_CAPACIDADE_M3',
            'type' => 'decimal',
            'len' => '10',
            'precision' => '2',
        ),
        'eixos' => array(
            'name' => 'eixos',
            'vname' => 'LBL_EIXOS',
            'type' => 'int',
            'len' => 2,
        ),
        
        // Documentação
        'crlv_validade' => array(
            'name' => 'crlv_validade',
            'vname' => 'LBL_CRLV_VALIDADE',
            'type' => 'date',
            'audited' => true,
        ),
        'seguro_validade' => array(
            'name' => 'seguro_validade',
            'vname' => 'LBL_SEGURO_VALIDADE',
            'type' => 'date',
        ),
        'seguro_apolice' => array(
            'name' => 'seguro_apolice',
            'vname' => 'LBL_SEGURO_APOLICE',
            'type' => 'varchar',
            'len' => 50,
        ),
        
        // Rastreamento
        'rastreador' => array(
            'name' => 'rastreador',
            'vname' => 'LBL_RASTREADOR',
            'type' => 'bool',
            'default' => '0',
        ),
        'rastreador_id' => array(
            'name' => 'rastreador_id',
            'vname' => 'LBL_RASTREADOR_ID',
            'type' => 'varchar',
            'len' => 50,
        ),
        
        // Manutenção
        'km_atual' => array(
            'name' => 'km_atual',
            'vname' => 'LBL_KM_ATUAL',
            'type' => 'int',
            'len' => 10,
        ),
        'ultima_manutencao' => array(
            'name' => 'ultima_manutencao',
            'vname' => 'LBL_ULTIMA_MANUTENCAO',
            'type' => 'date',
        ),
        'proxima_manutencao' => array(
            'name' => 'proxima_manutencao',
            'vname' => 'LBL_PROXIMA_MANUTENCAO',
            'type' => 'date',
        ),
        'km_proxima_manutencao' => array(
            'name' => 'km_proxima_manutencao',
            'vname' => 'LBL_KM_PROXIMA_MANUTENCAO',
            'type' => 'int',
            'len' => 10,
        ),
        
        // Status
        'status' => array(
            'name' => 'status',
            'vname' => 'LBL_STATUS',
            'type' => 'enum',
            'options' => 'veiculo_status_list',
            'len' => 20,
            'default' => 'disponivel',
            'required' => true,
            'audited' => true,
        ),
        'status_manutencao' => array(
            'name' => 'status_manutencao',
            'vname' => 'LBL_STATUS_MANUTENCAO',
            'type' => 'enum',
            'options' => 'veiculo_status_manutencao_list',
            'len' => 20,
            'default' => 'ok',
        ),
        
        // Propriedade
        'proprietario' => array(
            'name' => 'proprietario',
            'vname' => 'LBL_PROPRIETARIO',
            'type' => 'enum',
            'options' => 'veiculo_proprietario_list',
            'len' => 20,
            'default' => 'proprio',
        ),
        'proprietario_nome' => array(
            'name' => 'proprietario_nome',
            'vname' => 'LBL_PROPRIETARIO_NOME',
            'type' => 'varchar',
            'len' => 200,
        ),
        
        'observacoes' => array(
            'name' => 'observacoes',
            'vname' => 'LBL_OBSERVACOES',
            'type' => 'text',
        ),
        
        // Links
        'pedidos_link' => array(
            'name' => 'pedidos_link',
            'type' => 'link',
            'relationship' => 'veiculos_pedidos',
            'source' => 'non-db',
            'module' => 'PedidosFrete',
            'vname' => 'LBL_PEDIDOS',
        ),
        'assigned_user_link' => array(
            'name' => 'assigned_user_link',
            'type' => 'link',
            'relationship' => 'veiculos_assigned_user',
            'source' => 'non-db',
            'module' => 'Users',
            'vname' => 'LBL_ASSIGNED_TO_USER',
        ),
    ),
    
    'relationships' => array(
        'veiculos_pedidos' => array(
            'lhs_module' => 'Veiculos',
            'lhs_table' => 'veiculos',
            'lhs_key' => 'id',
            'rhs_module' => 'PedidosFrete',
            'rhs_table' => 'pedidos_frete',
            'rhs_key' => 'veiculo_id',
            'relationship_type' => 'one-to-many',
        ),
        'veiculos_assigned_user' => array(
            'lhs_module' => 'Users',
            'lhs_table' => 'users',
            'lhs_key' => 'id',
            'rhs_module' => 'Veiculos',
            'rhs_table' => 'veiculos',
            'rhs_key' => 'assigned_user_id',
            'relationship_type' => 'one-to-many',
        ),
    ),
    
    'indices' => array(
        array(
            'name' => 'idx_veiculos_placa',
            'type' => 'unique',
            'fields' => array('placa'),
        ),
        array(
            'name' => 'idx_veiculos_renavam',
            'type' => 'index',
            'fields' => array('renavam'),
        ),
        array(
            'name' => 'idx_veiculos_status',
            'type' => 'index',
            'fields' => array('status'),
        ),
        array(
            'name' => 'idx_veiculos_tipo',
            'type' => 'index',
            'fields' => array('tipo_veiculo'),
        ),
    ),
    
    'optimistic_locking' => true,
);

VardefManager::createVardef('Veiculos', 'Veiculos', array('basic', 'assignable', 'security_groups'));
