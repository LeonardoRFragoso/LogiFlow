<?php
/**
 * LogiFlow CRM - Módulo Entregas
 * Vardefs - Definição de campos
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

$dictionary['Entregas'] = array(
    'table' => 'entregas',
    'audited' => true,
    'unified_search' => true,
    'comment' => 'Registro de entregas e rastreamento',
    
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
        
        // ========================================
        // CAMPOS ESPECÍFICOS DE ENTREGA
        // ========================================
        
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
        
        // Status
        'status' => array(
            'name' => 'status',
            'vname' => 'LBL_STATUS',
            'type' => 'enum',
            'options' => 'entrega_status_list',
            'len' => 30,
            'default' => 'aguardando',
            'required' => true,
            'audited' => true,
        ),
        
        // Localização
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
        'local_descricao' => array(
            'name' => 'local_descricao',
            'vname' => 'LBL_LOCAL_DESCRICAO',
            'type' => 'varchar',
            'len' => 255,
        ),
        
        // Comprovante
        'recebedor_nome' => array(
            'name' => 'recebedor_nome',
            'vname' => 'LBL_RECEBEDOR_NOME',
            'type' => 'varchar',
            'len' => 200,
        ),
        'recebedor_documento' => array(
            'name' => 'recebedor_documento',
            'vname' => 'LBL_RECEBEDOR_DOCUMENTO',
            'type' => 'varchar',
            'len' => 20,
        ),
        'recebedor_parentesco' => array(
            'name' => 'recebedor_parentesco',
            'vname' => 'LBL_RECEBEDOR_PARENTESCO',
            'type' => 'varchar',
            'len' => 50,
        ),
        'foto_comprovante' => array(
            'name' => 'foto_comprovante',
            'vname' => 'LBL_FOTO_COMPROVANTE',
            'type' => 'image',
            'dbType' => 'varchar',
            'len' => 255,
        ),
        'assinatura' => array(
            'name' => 'assinatura',
            'vname' => 'LBL_ASSINATURA',
            'type' => 'image',
            'dbType' => 'varchar',
            'len' => 255,
        ),
        
        // Data do evento
        'data_evento' => array(
            'name' => 'data_evento',
            'vname' => 'LBL_DATA_EVENTO',
            'type' => 'datetimecombo',
            'dbType' => 'datetime',
            'required' => true,
        ),
        
        // Tentativas
        'tentativa_numero' => array(
            'name' => 'tentativa_numero',
            'vname' => 'LBL_TENTATIVA_NUMERO',
            'type' => 'int',
            'len' => 2,
            'default' => 1,
        ),
        'motivo_insucesso' => array(
            'name' => 'motivo_insucesso',
            'vname' => 'LBL_MOTIVO_INSUCESSO',
            'type' => 'enum',
            'options' => 'entrega_motivo_insucesso_list',
            'len' => 50,
        ),
        
        'observacao' => array(
            'name' => 'observacao',
            'vname' => 'LBL_OBSERVACAO',
            'type' => 'text',
        ),
        
        // Links
        'pedido_link' => array(
            'name' => 'pedido_link',
            'type' => 'link',
            'relationship' => 'pedidos_entregas',
            'source' => 'non-db',
            'module' => 'PedidosFrete',
            'vname' => 'LBL_PEDIDO',
        ),
        'assigned_user_link' => array(
            'name' => 'assigned_user_link',
            'type' => 'link',
            'relationship' => 'entregas_assigned_user',
            'source' => 'non-db',
            'module' => 'Users',
            'vname' => 'LBL_ASSIGNED_TO_USER',
        ),
    ),
    
    'relationships' => array(
        'pedidos_entregas' => array(
            'lhs_module' => 'PedidosFrete',
            'lhs_table' => 'pedidos_frete',
            'lhs_key' => 'id',
            'rhs_module' => 'Entregas',
            'rhs_table' => 'entregas',
            'rhs_key' => 'pedido_id',
            'relationship_type' => 'one-to-many',
        ),
        'entregas_assigned_user' => array(
            'lhs_module' => 'Users',
            'lhs_table' => 'users',
            'lhs_key' => 'id',
            'rhs_module' => 'Entregas',
            'rhs_table' => 'entregas',
            'rhs_key' => 'assigned_user_id',
            'relationship_type' => 'one-to-many',
        ),
    ),
    
    'indices' => array(
        array(
            'name' => 'idx_entregas_pedido',
            'type' => 'index',
            'fields' => array('pedido_id'),
        ),
        array(
            'name' => 'idx_entregas_status',
            'type' => 'index',
            'fields' => array('status'),
        ),
        array(
            'name' => 'idx_entregas_data',
            'type' => 'index',
            'fields' => array('data_evento'),
        ),
    ),
    
    'optimistic_locking' => true,
);

VardefManager::createVardef('Entregas', 'Entregas', array('basic', 'assignable', 'security_groups'));
