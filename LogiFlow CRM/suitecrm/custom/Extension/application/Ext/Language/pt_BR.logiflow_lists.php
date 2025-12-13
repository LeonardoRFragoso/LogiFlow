<?php
/**
 * LogiFlow CRM - Listas de Dropdown
 * Português Brasil
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

// Status da Cotação
$app_list_strings['cotacao_status_list'] = array(
    '' => '',
    'aberta' => 'Aberta',
    'em_negociacao' => 'Em Negociação',
    'aprovada' => 'Aprovada',
    'perdida' => 'Perdida',
    'expirada' => 'Expirada',
    'cancelada' => 'Cancelada',
);

// Tipo de Carga
$app_list_strings['tipo_carga_list'] = array(
    '' => '',
    'geral' => 'Carga Geral',
    'fracionada' => 'Fracionada',
    'lotacao' => 'Lotação Completa',
    'container' => 'Container',
    'granel_solido' => 'Granel Sólido',
    'granel_liquido' => 'Granel Líquido',
    'refrigerada' => 'Refrigerada',
    'perigosa' => 'Carga Perigosa',
    'viva' => 'Carga Viva',
    'indivisivel' => 'Carga Indivisível',
    'mudanca' => 'Mudança',
);

// Modal de Transporte
$app_list_strings['modal_transporte_list'] = array(
    '' => '',
    'rodoviario' => 'Rodoviário',
    'aereo' => 'Aéreo',
    'maritimo' => 'Marítimo',
    'ferroviario' => 'Ferroviário',
    'fluvial' => 'Fluvial',
    'multimodal' => 'Multimodal',
);

// Motivo de Perda
$app_list_strings['motivo_perda_list'] = array(
    '' => '',
    'preco' => 'Preço',
    'prazo' => 'Prazo',
    'concorrente' => 'Perdeu para Concorrente',
    'desistencia' => 'Cliente Desistiu',
    'sem_retorno' => 'Sem Retorno do Cliente',
    'fora_area' => 'Fora da Área de Atuação',
    'outro' => 'Outro',
);

// Status Operacional do Pedido
$app_list_strings['status_operacional_list'] = array(
    '' => '',
    'em_planejamento' => 'Em Planejamento',
    'aguardando_coleta' => 'Aguardando Coleta',
    'em_coleta' => 'Em Coleta',
    'coletado' => 'Coletado',
    'em_transito' => 'Em Trânsito',
    'em_transferencia' => 'Em Transferência',
    'saiu_entrega' => 'Saiu para Entrega',
    'entregue' => 'Entregue',
    'tentativa_entrega' => 'Tentativa de Entrega',
    'devolvido' => 'Devolvido',
    'cancelado' => 'Cancelado',
);

// Status SLA
$app_list_strings['sla_status_list'] = array(
    '' => '',
    'verde' => 'No Prazo',
    'amarelo' => 'Atenção',
    'vermelho' => 'Atrasado',
);

// Status da Entrega
$app_list_strings['entrega_status_list'] = array(
    '' => '',
    'aguardando' => 'Aguardando',
    'em_rota' => 'Em Rota',
    'chegou_destino' => 'Chegou ao Destino',
    'entregue' => 'Entregue',
    'entregue_parcial' => 'Entregue Parcialmente',
    'ausente' => 'Destinatário Ausente',
    'recusado' => 'Recusado',
    'endereco_incorreto' => 'Endereço Incorreto',
    'avariado' => 'Avariado',
    'devolvido' => 'Devolvido',
);

// Tipo de Ocorrência
$app_list_strings['tipo_ocorrencia_list'] = array(
    '' => '',
    'atraso' => 'Atraso',
    'avaria' => 'Avaria',
    'extravio' => 'Extravio',
    'roubo' => 'Roubo/Furto',
    'acidente' => 'Acidente',
    'devolucao' => 'Devolução',
    'recusa' => 'Recusa',
    'reentrega' => 'Reentrega',
    'fiscalizacao' => 'Fiscalização',
    'outro' => 'Outro',
);

// Status da Ocorrência
$app_list_strings['ocorrencia_status_list'] = array(
    '' => '',
    'aberta' => 'Aberta',
    'em_analise' => 'Em Análise',
    'resolvida' => 'Resolvida',
    'cancelada' => 'Cancelada',
);

// Status do Motorista
$app_list_strings['motorista_status_list'] = array(
    '' => '',
    'ativo' => 'Ativo',
    'inativo' => 'Inativo',
    'ferias' => 'Férias',
    'afastado' => 'Afastado',
    'desligado' => 'Desligado',
);

// Categoria CNH
$app_list_strings['categoria_cnh_list'] = array(
    '' => '',
    'A' => 'A - Motocicleta',
    'B' => 'B - Carro',
    'C' => 'C - Caminhão',
    'D' => 'D - Ônibus',
    'E' => 'E - Carreta',
    'AB' => 'AB',
    'AC' => 'AC',
    'AD' => 'AD',
    'AE' => 'AE',
);

// Tipo de Veículo
$app_list_strings['tipo_veiculo_list'] = array(
    '' => '',
    'moto' => 'Motocicleta',
    'fiorino' => 'Fiorino/Kangoo',
    'van' => 'Van',
    'vuc' => 'VUC',
    'toco' => 'Caminhão Toco',
    'truck' => 'Caminhão Truck',
    'carreta' => 'Carreta',
    'bitrem' => 'Bitrem',
    'rodotrem' => 'Rodotrem',
);

// Status do Veículo
$app_list_strings['veiculo_status_list'] = array(
    '' => '',
    'disponivel' => 'Disponível',
    'em_viagem' => 'Em Viagem',
    'manutencao' => 'Em Manutenção',
    'reservado' => 'Reservado',
    'inativo' => 'Inativo',
);

// Tipo de Manutenção
$app_list_strings['tipo_manutencao_list'] = array(
    '' => '',
    'preventiva' => 'Preventiva',
    'corretiva' => 'Corretiva',
    'revisao' => 'Revisão',
    'troca_pneu' => 'Troca de Pneu',
    'troca_oleo' => 'Troca de Óleo',
    'documentacao' => 'Documentação',
);

// Condição de Pagamento
$app_list_strings['condicao_pagamento_list'] = array(
    '' => '',
    'a_vista' => 'À Vista',
    '7_dias' => '7 dias',
    '14_dias' => '14 dias',
    '21_dias' => '21 dias',
    '28_dias' => '28 dias',
    '30_dias' => '30 dias',
    '45_dias' => '45 dias',
    '60_dias' => '60 dias',
    'faturado' => 'Faturado',
);

// Estados do Brasil
$app_list_strings['estados_brasil_list'] = array(
    '' => '',
    'AC' => 'Acre',
    'AL' => 'Alagoas',
    'AP' => 'Amapá',
    'AM' => 'Amazonas',
    'BA' => 'Bahia',
    'CE' => 'Ceará',
    'DF' => 'Distrito Federal',
    'ES' => 'Espírito Santo',
    'GO' => 'Goiás',
    'MA' => 'Maranhão',
    'MT' => 'Mato Grosso',
    'MS' => 'Mato Grosso do Sul',
    'MG' => 'Minas Gerais',
    'PA' => 'Pará',
    'PB' => 'Paraíba',
    'PR' => 'Paraná',
    'PE' => 'Pernambuco',
    'PI' => 'Piauí',
    'RJ' => 'Rio de Janeiro',
    'RN' => 'Rio Grande do Norte',
    'RS' => 'Rio Grande do Sul',
    'RO' => 'Rondônia',
    'RR' => 'Roraima',
    'SC' => 'Santa Catarina',
    'SP' => 'São Paulo',
    'SE' => 'Sergipe',
    'TO' => 'Tocantins',
);
