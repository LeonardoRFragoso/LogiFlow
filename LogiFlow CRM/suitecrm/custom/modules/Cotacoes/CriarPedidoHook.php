<?php
/**
 * LogiFlow CRM - Logic Hook: Criar Pedido quando Cotação é Aprovada
 * 
 * Este hook é disparado após salvar uma cotação.
 * Se o status mudar para "aprovada", cria automaticamente um pedido de frete.
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

class CriarPedidoHook
{
    /**
     * Executa o hook após salvar a cotação
     * 
     * @param SugarBean $bean O bean da cotação
     * @param string $event O evento (after_save)
     * @param array $arguments Argumentos adicionais
     */
    public function executar($bean, $event, $arguments)
    {
        global $current_user;
        
        // Verificar se é uma atualização (não criação)
        if (empty($arguments['isUpdate'])) {
            return;
        }
        
        // Verificar se o status mudou para "aprovada"
        if ($bean->status !== 'aprovada') {
            return;
        }
        
        // Verificar se o status anterior era diferente de "aprovada"
        $dataChanges = $bean->fetched_row ?? [];
        $statusAnterior = $dataChanges['status'] ?? '';
        
        if ($statusAnterior === 'aprovada') {
            // Status já era aprovada, não criar novo pedido
            return;
        }
        
        // Verificar se já existe um pedido para esta cotação
        $pedidoExistente = $this->verificarPedidoExistente($bean->id);
        if ($pedidoExistente) {
            $GLOBALS['log']->info("LogiFlow: Pedido já existe para cotação {$bean->id}");
            return;
        }
        
        // Criar o pedido de frete
        $this->criarPedido($bean);
    }
    
    /**
     * Verifica se já existe um pedido para a cotação
     * 
     * @param string $cotacaoId ID da cotação
     * @return bool
     */
    private function verificarPedidoExistente($cotacaoId)
    {
        $query = new SugarQuery();
        $query->select(array('id'));
        $query->from(BeanFactory::newBean('PedidosFrete'));
        $query->where()->equals('cotacao_id', $cotacaoId);
        $query->where()->equals('deleted', 0);
        $query->limit(1);
        
        $results = $query->execute();
        
        return !empty($results);
    }
    
    /**
     * Cria um novo pedido de frete baseado na cotação
     * 
     * @param SugarBean $cotacao Bean da cotação aprovada
     */
    private function criarPedido($cotacao)
    {
        global $current_user;
        
        try {
            // Criar novo bean de pedido
            $pedido = BeanFactory::newBean('PedidosFrete');
            
            // Gerar número do pedido
            $numeroPedido = $this->gerarNumeroPedido();
            
            // Preencher campos básicos
            $pedido->name = "Pedido {$numeroPedido} - {$cotacao->cliente_name}";
            $pedido->numero_pedido = $numeroPedido;
            $pedido->data_pedido = date('Y-m-d');
            
            // Relacionamentos
            $pedido->cotacao_id = $cotacao->id;
            $pedido->cliente_id = $cotacao->cliente_id;
            
            // Origem
            $pedido->origem_cep = $cotacao->origem_cep;
            $pedido->origem_endereco = $cotacao->origem_endereco;
            $pedido->origem_cidade = $cotacao->origem_cidade;
            $pedido->origem_uf = $cotacao->origem_uf;
            
            // Destino
            $pedido->destino_cep = $cotacao->destino_cep;
            $pedido->destino_endereco = $cotacao->destino_endereco;
            $pedido->destino_cidade = $cotacao->destino_cidade;
            $pedido->destino_uf = $cotacao->destino_uf;
            $pedido->destinatario_nome = $cotacao->contato_nome ?? '';
            $pedido->destinatario_telefone = $cotacao->contato_telefone ?? '';
            
            // Carga
            $pedido->tipo_carga = $cotacao->tipo_carga;
            $pedido->peso_kg = $cotacao->peso_kg;
            $pedido->cubagem_m3 = $cotacao->cubagem_m3;
            $pedido->quantidade_volumes = $cotacao->quantidade_volumes ?? 1;
            $pedido->valor_mercadoria = $cotacao->valor_mercadoria;
            
            // Valores
            $pedido->valor_frete = $cotacao->valor_frete;
            $pedido->valor_seguro = $cotacao->valor_seguro ?? 0;
            $pedido->valor_adicional = $cotacao->valor_adicional ?? 0;
            
            // Previsão de entrega baseada no prazo estimado
            if (!empty($cotacao->prazo_estimado)) {
                $previsao = date('Y-m-d', strtotime("+{$cotacao->prazo_estimado} days"));
                $pedido->previsao_entrega = $previsao;
            } else {
                // Padrão: 5 dias úteis
                $pedido->previsao_entrega = date('Y-m-d', strtotime('+5 days'));
            }
            
            // Status inicial
            $pedido->status = 'em_planejamento';
            $pedido->sla_status = 'verde';
            
            // Observações
            $pedido->observacoes = "Pedido gerado automaticamente a partir da Cotação {$cotacao->numero_cotacao}";
            
            // Atribuição
            $pedido->assigned_user_id = $cotacao->assigned_user_id ?? $current_user->id;
            
            // Salvar pedido
            $pedido->save();
            
            // Log de sucesso
            $GLOBALS['log']->info(
                "LogiFlow: Pedido {$numeroPedido} criado automaticamente " .
                "a partir da cotação {$cotacao->numero_cotacao} (ID: {$cotacao->id})"
            );
            
        } catch (Exception $e) {
            $GLOBALS['log']->error(
                "LogiFlow: Erro ao criar pedido para cotação {$cotacao->id}: " . 
                $e->getMessage()
            );
        }
    }
    
    /**
     * Gera um número único para o pedido
     * Formato: PED-YYYYMMDD-XXXX
     * 
     * @return string
     */
    private function gerarNumeroPedido()
    {
        $data = date('Ymd');
        
        // Buscar último número do dia
        $query = new SugarQuery();
        $query->select(array('numero_pedido'));
        $query->from(BeanFactory::newBean('PedidosFrete'));
        $query->where()->starts('numero_pedido', "PED-{$data}");
        $query->orderBy('numero_pedido', 'DESC');
        $query->limit(1);
        
        $results = $query->execute();
        
        if (!empty($results)) {
            // Extrair sequencial e incrementar
            $ultimo = $results[0]['numero_pedido'];
            preg_match('/PED-\d{8}-(\d{4})/', $ultimo, $matches);
            $sequencial = isset($matches[1]) ? intval($matches[1]) + 1 : 1;
        } else {
            $sequencial = 1;
        }
        
        return sprintf("PED-%s-%04d", $data, $sequencial);
    }
}
