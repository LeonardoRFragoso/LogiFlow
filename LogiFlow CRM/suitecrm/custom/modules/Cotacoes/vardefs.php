<?php
/**
 * LogiFlow CRM - Módulo Cotações
 * Definição de campos (vardefs)
 */

if (!defined('sugarEntry') || !sugarEntry) {
    die('Not A Valid Entry Point');
}

$dictionary['Cotacoes'] = array(
    'table' => 'cotacoes',
    'audited' => true,
    'unified_search' => true,
    'comment' => 'Cotações de frete para clientes',
    
    'fields' => array(
        // Campos básicos herdados
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
            'len' => 150,
            'required' => true,
            'audited' => true,
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
            'default' => 0,
        ),
        'assigned_user_id' => array(
            'name' => 'assigned_user_id',
            'vname' => 'LBL_ASSIGNED_USER_ID',
            'type' => 'id',
        ),
        
        // === CAMPOS ESPECÍFICOS DE COTAÇÃO ===
        
        // Relacionamento com Cliente (Accounts)
        'account_id' => array(
            'name' => 'account_id',
            'vname' => 'LBL_ACCOUNT_ID',
            'type' => 'id',
            'reportable' => false,
        ),
        'account_name' => array(
            'name' => 'account_name',
            'vname' => 'LBL_ACCOUNT_NAME',
            'type' => 'relate',
            'source' => 'non-db',
            'len' => 100,
            'id_name' => 'account_id',
            'module' => 'Accounts',
            'link' => 'accounts',
            'rname' => 'name',
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
        
        // Carga
        'tipo_carga' => array(
            'name' => 'tipo_carga',
            'vname' => 'LBL_TIPO_CARGA',
            'type' => 'enum',
            'options' => 'tipo_carga_list',
            'len' => 30,
            'required' => true,
        ),
        'peso_kg' => array(
            'name' => 'peso_kg',
            'vname' => 'LBL_PESO_KG',
            'type' => 'decimal',
            'len' => '10,2',
            'required' => true,
        ),
        'cubagem_m3' => array(
            'name' => 'cubagem_m3',
            'vname' => 'LBL_CUBAGEM_M3',
            'type' => 'decimal',
            'len' => '10,3',
        ),
        'quantidade_volumes' => array(
            'name' => 'quantidade_volumes',
            'vname' => 'LBL_QUANTIDADE_VOLUMES',
            'type' => 'int',
            'len' => 5,
            'default' => 1,
        ),
        'valor_mercadoria' => array(
            'name' => 'valor_mercadoria',
            'vname' => 'LBL_VALOR_MERCADORIA',
            'type' => 'currency',
            'len' => '12,2',
        ),
        
        // Valores
        'valor_proposta' => array(
            'name' => 'valor_proposta',
            'vname' => 'LBL_VALOR_PROPOSTA',
            'type' => 'currency',
            'len' => '12,2',
            'required' => true,
            'audited' => true,
        ),
        'prazo_estimado' => array(
            'name' => 'prazo_estimado',
            'vname' => 'LBL_PRAZO_ESTIMADO',
            'type' => 'int',
            'len' => 3,
            'comment' => 'Prazo em dias',
        ),
        
        // Transporte
        'modal' => array(
            'name' => 'modal',
            'vname' => 'LBL_MODAL',
            'type' => 'enum',
            'options' => 'modal_transporte_list',
            'len' => 20,
            'default' => 'rodoviario',
        ),
        
        // Datas
        'validade' => array(
            'name' => 'validade',
            'vname' => 'LBL_VALIDADE',
            'type' => 'date',
        ),
        
        // Status
        'status' => array(
            'name' => 'status',
            'vname' => 'LBL_STATUS',
            'type' => 'enum',
            'options' => 'cotacao_status_list',
            'len' => 20,
            'default' => 'aberta',
            'audited' => true,
        ),
        
        // Observações
        'observacoes' => array(
            'name' => 'observacoes',
            'vname' => 'LBL_OBSERVACOES',
            'type' => 'text',
        ),
    ),
    
    'relationships' => array(
        'cotacoes_accounts' => array(
            'lhs_module' => 'Accounts',
            'lhs_table' => 'accounts',
            'lhs_key' => 'id',
            'rhs_module' => 'Cotacoes',
            'rhs_table' => 'cotacoes',
            'rhs_key' => 'account_id',
            'relationship_type' => 'one-to-many',
        ),
    ),
    
    'indices' => array(
        array(
            'name' => 'idx_cotacoes_account',
            'type' => 'index',
            'fields' => array('account_id'),
        ),
        array(
            'name' => 'idx_cotacoes_status',
            'type' => 'index',
            'fields' => array('status'),
        ),
        array(
            'name' => 'idx_cotacoes_assigned',
            'type' => 'index',
            'fields' => array('assigned_user_id'),
        ),
    ),
);

VardefManager::createVardef('Cotacoes', 'Cotacoes', array('basic', 'assignable', 'security_groups'));
