<?php
/**
 * LogiFlow CRM - Dropdown Lists
 * Listas de opções para campos enum
 * Idioma: Português Brasil
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

// ==========================================
// COTAÇÕES
// ==========================================
$app_list_strings['cotacao_status_list'] = array(
    'aberta' => 'Aberta',
    'enviada' => 'Enviada ao Cliente',
    'em_negociacao' => 'Em Negociação',
    'aprovada' => 'Aprovada',
    'perdida' => 'Perdida',
    'cancelada' => 'Cancelada',
    'expirada' => 'Expirada',
);

$app_list_strings['motivo_perda_list'] = array(
    '' => '',
    'preco' => 'Preço',
    'prazo' => 'Prazo',
    'concorrencia' => 'Concorrência',
    'desistencia' => 'Desistência do Cliente',
    'outros' => 'Outros',
);

// ==========================================
// TIPO DE CARGA
// ==========================================
$app_list_strings['tipo_carga_list'] = array(
    'geral' => 'Carga Geral',
    'fracionada' => 'Carga Fracionada',
    'completa' => 'Carga Completa',
    'granel_solido' => 'Granel Sólido',
    'granel_liquido' => 'Granel Líquido',
    'refrigerada' => 'Refrigerada',
    'perigosa' => 'Perigosa',
    'viva' => 'Carga Viva',
    'indivisivel' => 'Indivisível',
    'container' => 'Container',
    'mudanca' => 'Mudança',
    'veiculo' => 'Veículo',
);

// ==========================================
// MODAL DE TRANSPORTE
// ==========================================
$app_list_strings['modal_transporte_list'] = array(
    'rodoviario' => 'Rodoviário',
    'aereo' => 'Aéreo',
    'maritimo' => 'Marítimo',
    'ferroviario' => 'Ferroviário',
    'fluvial' => 'Fluvial',
    'multimodal' => 'Multimodal',
);

// ==========================================
// PEDIDOS DE FRETE
// ==========================================
$app_list_strings['pedido_status_list'] = array(
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

$app_list_strings['sla_status_list'] = array(
    'verde' => 'No Prazo',
    'amarelo' => 'Atenção',
    'vermelho' => 'Atrasado',
);

// ==========================================
// CT-e
// ==========================================
$app_list_strings['cte_status_list'] = array(
    '' => '',
    'pendente' => 'Pendente',
    'processando' => 'Processando',
    'autorizado' => 'Autorizado',
    'rejeitado' => 'Rejeitado',
    'cancelado' => 'Cancelado',
    'inutilizado' => 'Inutilizado',
);

// ==========================================
// MOTORISTAS
// ==========================================
$app_list_strings['cnh_categoria_list'] = array(
    'A' => 'A - Moto',
    'B' => 'B - Carro',
    'C' => 'C - Caminhão',
    'D' => 'D - Ônibus',
    'E' => 'E - Carreta',
    'AB' => 'AB',
    'AC' => 'AC',
    'AD' => 'AD',
    'AE' => 'AE',
);

$app_list_strings['motorista_status_list'] = array(
    'ativo' => 'Ativo',
    'inativo' => 'Inativo',
    'ferias' => 'Férias',
    'afastado' => 'Afastado',
    'desligado' => 'Desligado',
);

$app_list_strings['motorista_disponibilidade_list'] = array(
    'disponivel' => 'Disponível',
    'em_viagem' => 'Em Viagem',
    'indisponivel' => 'Indisponível',
    'descanso' => 'Em Descanso',
);

// ==========================================
// VEÍCULOS
// ==========================================
$app_list_strings['tipo_veiculo_list'] = array(
    'vuc' => 'VUC',
    'toco' => 'Toco',
    'truck' => 'Truck',
    'carreta_simples' => 'Carreta Simples',
    'carreta_ls' => 'Carreta LS',
    'bitrem' => 'Bitrem',
    'rodotrem' => 'Rodotrem',
    'van' => 'Van',
    'fiorino' => 'Fiorino',
    'moto' => 'Moto',
    'utilitario' => 'Utilitário',
);

$app_list_strings['combustivel_list'] = array(
    'diesel' => 'Diesel',
    'diesel_s10' => 'Diesel S10',
    'gasolina' => 'Gasolina',
    'etanol' => 'Etanol',
    'flex' => 'Flex',
    'gnv' => 'GNV',
    'eletrico' => 'Elétrico',
);

$app_list_strings['veiculo_status_list'] = array(
    'disponivel' => 'Disponível',
    'em_viagem' => 'Em Viagem',
    'manutencao' => 'Em Manutenção',
    'inativo' => 'Inativo',
    'vendido' => 'Vendido',
);

$app_list_strings['veiculo_status_manutencao_list'] = array(
    'ok' => 'OK',
    'atencao' => 'Atenção',
    'critico' => 'Crítico',
    'em_manutencao' => 'Em Manutenção',
);

$app_list_strings['veiculo_proprietario_list'] = array(
    'proprio' => 'Próprio',
    'terceiro' => 'Terceiro',
    'agregado' => 'Agregado',
    'alugado' => 'Alugado',
);

// ==========================================
// ENTREGAS
// ==========================================
$app_list_strings['entrega_status_list'] = array(
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

$app_list_strings['entrega_motivo_insucesso_list'] = array(
    '' => '',
    'ausente' => 'Destinatário Ausente',
    'recusado' => 'Recusado pelo Destinatário',
    'endereco_incorreto' => 'Endereço Incorreto/Não Encontrado',
    'local_fechado' => 'Local Fechado',
    'sem_dinheiro' => 'Sem Dinheiro para Pagamento',
    'avaria' => 'Mercadoria Avariada',
    'falta' => 'Mercadoria em Falta',
    'documentacao' => 'Problema com Documentação',
    'outros' => 'Outros',
);

// ==========================================
// OCORRÊNCIAS
// ==========================================
$app_list_strings['ocorrencia_tipo_list'] = array(
    'avaria' => 'Avaria',
    'atraso' => 'Atraso',
    'extravio' => 'Extravio',
    'roubo' => 'Roubo/Furto',
    'acidente' => 'Acidente',
    'retorno' => 'Retorno',
    'sinistro' => 'Sinistro',
    'reclamacao' => 'Reclamação do Cliente',
    'outros' => 'Outros',
);

$app_list_strings['ocorrencia_categoria_list'] = array(
    '' => '',
    'carga' => 'Relacionada à Carga',
    'veiculo' => 'Relacionada ao Veículo',
    'motorista' => 'Relacionada ao Motorista',
    'cliente' => 'Relacionada ao Cliente',
    'operacional' => 'Operacional',
    'administrativa' => 'Administrativa',
);

$app_list_strings['ocorrencia_gravidade_list'] = array(
    'baixa' => 'Baixa',
    'media' => 'Média',
    'alta' => 'Alta',
    'critica' => 'Crítica',
);

$app_list_strings['ocorrencia_status_list'] = array(
    'aberta' => 'Aberta',
    'em_analise' => 'Em Análise',
    'em_tratamento' => 'Em Tratamento',
    'aguardando_cliente' => 'Aguardando Cliente',
    'resolvida' => 'Resolvida',
    'encerrada' => 'Encerrada',
);

// ==========================================
// UFs BRASIL
// ==========================================
$app_list_strings['uf_brasil_list'] = array(
    'AC' => 'AC', 'AL' => 'AL', 'AP' => 'AP', 'AM' => 'AM',
    'BA' => 'BA', 'CE' => 'CE', 'DF' => 'DF', 'ES' => 'ES',
    'GO' => 'GO', 'MA' => 'MA', 'MT' => 'MT', 'MS' => 'MS',
    'MG' => 'MG', 'PA' => 'PA', 'PB' => 'PB', 'PR' => 'PR',
    'PE' => 'PE', 'PI' => 'PI', 'RJ' => 'RJ', 'RN' => 'RN',
    'RS' => 'RS', 'RO' => 'RO', 'RR' => 'RR', 'SC' => 'SC',
    'SP' => 'SP', 'SE' => 'SE', 'TO' => 'TO',
);
