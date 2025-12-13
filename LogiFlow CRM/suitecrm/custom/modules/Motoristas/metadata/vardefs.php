<?php
/**
 * LogiFlow CRM - Módulo Motoristas
 * Vardefs - Definição de campos
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

$dictionary['Motoristas'] = array(
    'table' => 'motoristas',
    'audited' => true,
    'unified_search' => true,
    'comment' => 'Cadastro de motoristas',
    
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
            'len' => 150,
            'unified_search' => true,
            'required' => true,
            'comment' => 'Nome completo do motorista',
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
        // CAMPOS ESPECÍFICOS DE MOTORISTA
        // ========================================
        
        'cpf' => array(
            'name' => 'cpf',
            'vname' => 'LBL_CPF',
            'type' => 'varchar',
            'len' => 14,
            'unified_search' => true,
            'required' => true,
        ),
        'rg' => array(
            'name' => 'rg',
            'vname' => 'LBL_RG',
            'type' => 'varchar',
            'len' => 20,
        ),
        
        // CNH
        'cnh_numero' => array(
            'name' => 'cnh_numero',
            'vname' => 'LBL_CNH_NUMERO',
            'type' => 'varchar',
            'len' => 20,
            'required' => true,
        ),
        'cnh_categoria' => array(
            'name' => 'cnh_categoria',
            'vname' => 'LBL_CNH_CATEGORIA',
            'type' => 'enum',
            'options' => 'cnh_categoria_list',
            'len' => 5,
            'required' => true,
        ),
        'cnh_validade' => array(
            'name' => 'cnh_validade',
            'vname' => 'LBL_CNH_VALIDADE',
            'type' => 'date',
            'required' => true,
            'audited' => true,
        ),
        'cnh_uf_emissao' => array(
            'name' => 'cnh_uf_emissao',
            'vname' => 'LBL_CNH_UF_EMISSAO',
            'type' => 'varchar',
            'len' => 2,
        ),
        
        // Contato
        'celular' => array(
            'name' => 'celular',
            'vname' => 'LBL_CELULAR',
            'type' => 'phone',
            'dbType' => 'varchar',
            'len' => 20,
            'required' => true,
        ),
        'telefone_emergencia' => array(
            'name' => 'telefone_emergencia',
            'vname' => 'LBL_TELEFONE_EMERGENCIA',
            'type' => 'phone',
            'dbType' => 'varchar',
            'len' => 20,
        ),
        'email' => array(
            'name' => 'email',
            'vname' => 'LBL_EMAIL',
            'type' => 'varchar',
            'len' => 255,
        ),
        
        // Endereço
        'endereco' => array(
            'name' => 'endereco',
            'vname' => 'LBL_ENDERECO',
            'type' => 'varchar',
            'len' => 255,
        ),
        'cidade' => array(
            'name' => 'cidade',
            'vname' => 'LBL_CIDADE',
            'type' => 'varchar',
            'len' => 100,
        ),
        'uf' => array(
            'name' => 'uf',
            'vname' => 'LBL_UF',
            'type' => 'varchar',
            'len' => 2,
        ),
        'cep' => array(
            'name' => 'cep',
            'vname' => 'LBL_CEP',
            'type' => 'varchar',
            'len' => 10,
        ),
        
        // Dados bancários
        'banco' => array(
            'name' => 'banco',
            'vname' => 'LBL_BANCO',
            'type' => 'varchar',
            'len' => 100,
        ),
        'agencia' => array(
            'name' => 'agencia',
            'vname' => 'LBL_AGENCIA',
            'type' => 'varchar',
            'len' => 20,
        ),
        'conta' => array(
            'name' => 'conta',
            'vname' => 'LBL_CONTA',
            'type' => 'varchar',
            'len' => 30,
        ),
        'pix' => array(
            'name' => 'pix',
            'vname' => 'LBL_PIX',
            'type' => 'varchar',
            'len' => 100,
        ),
        
        // Status
        'status' => array(
            'name' => 'status',
            'vname' => 'LBL_STATUS',
            'type' => 'enum',
            'options' => 'motorista_status_list',
            'len' => 20,
            'default' => 'ativo',
            'required' => true,
            'audited' => true,
        ),
        'disponibilidade' => array(
            'name' => 'disponibilidade',
            'vname' => 'LBL_DISPONIBILIDADE',
            'type' => 'enum',
            'options' => 'motorista_disponibilidade_list',
            'len' => 20,
            'default' => 'disponivel',
        ),
        
        // Datas
        'data_admissao' => array(
            'name' => 'data_admissao',
            'vname' => 'LBL_DATA_ADMISSAO',
            'type' => 'date',
        ),
        'data_nascimento' => array(
            'name' => 'data_nascimento',
            'vname' => 'LBL_DATA_NASCIMENTO',
            'type' => 'date',
        ),
        
        // Foto
        'foto' => array(
            'name' => 'foto',
            'vname' => 'LBL_FOTO',
            'type' => 'image',
            'dbType' => 'varchar',
            'len' => 255,
        ),
        
        // Observações
        'observacoes' => array(
            'name' => 'observacoes',
            'vname' => 'LBL_OBSERVACOES',
            'type' => 'text',
        ),
        
        // Links
        'pedidos_link' => array(
            'name' => 'pedidos_link',
            'type' => 'link',
            'relationship' => 'motoristas_pedidos',
            'source' => 'non-db',
            'module' => 'PedidosFrete',
            'vname' => 'LBL_PEDIDOS',
        ),
        'assigned_user_link' => array(
            'name' => 'assigned_user_link',
            'type' => 'link',
            'relationship' => 'motoristas_assigned_user',
            'source' => 'non-db',
            'module' => 'Users',
            'vname' => 'LBL_ASSIGNED_TO_USER',
        ),
    ),
    
    'relationships' => array(
        'motoristas_pedidos' => array(
            'lhs_module' => 'Motoristas',
            'lhs_table' => 'motoristas',
            'lhs_key' => 'id',
            'rhs_module' => 'PedidosFrete',
            'rhs_table' => 'pedidos_frete',
            'rhs_key' => 'motorista_id',
            'relationship_type' => 'one-to-many',
        ),
        'motoristas_assigned_user' => array(
            'lhs_module' => 'Users',
            'lhs_table' => 'users',
            'lhs_key' => 'id',
            'rhs_module' => 'Motoristas',
            'rhs_table' => 'motoristas',
            'rhs_key' => 'assigned_user_id',
            'relationship_type' => 'one-to-many',
        ),
    ),
    
    'indices' => array(
        array(
            'name' => 'idx_motoristas_cpf',
            'type' => 'unique',
            'fields' => array('cpf'),
        ),
        array(
            'name' => 'idx_motoristas_cnh',
            'type' => 'index',
            'fields' => array('cnh_numero'),
        ),
        array(
            'name' => 'idx_motoristas_status',
            'type' => 'index',
            'fields' => array('status'),
        ),
        array(
            'name' => 'idx_motoristas_cnh_validade',
            'type' => 'index',
            'fields' => array('cnh_validade'),
        ),
    ),
    
    'optimistic_locking' => true,
);

VardefManager::createVardef('Motoristas', 'Motoristas', array('basic', 'assignable', 'security_groups'));
