<?php
/**
 * LogiFlow CRM - Logic Hooks do Módulo Cotações
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

$hook_version = 1;
$hook_array = array();

$hook_array['after_save'] = array();
$hook_array['after_save'][] = array(
    1,
    'Criar Pedido quando Cotação Aprovada',
    'custom/modules/Cotacoes/CriarPedidoHook.php',
    'CriarPedidoHook',
    'executar'
);
