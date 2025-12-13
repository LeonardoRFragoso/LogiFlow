"""
LogiFlow CRM - Integração Focus NFe
Serviço para emissão de CT-e e MDF-e
"""

import requests
import json
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from decouple import config


class FocusNFeClient:
    """Cliente para API Focus NFe"""
    
    BASE_URL_PROD = 'https://api.focusnfe.com.br'
    BASE_URL_HOMOLOG = 'https://homologacao.focusnfe.com.br'
    
    def __init__(self, token=None, ambiente='homologacao'):
        self.token = token or config('FOCUSNFE_TOKEN', default='')
        self.ambiente = ambiente
        self.base_url = self.BASE_URL_HOMOLOG if ambiente == 'homologacao' else self.BASE_URL_PROD
    
    def _request(self, method, endpoint, data=None):
        """Executa requisição na API"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        auth = (self.token, '')
        
        response = requests.request(
            method=method,
            url=url,
            auth=auth,
            headers=headers,
            json=data,
            timeout=60
        )
        
        return response.json() if response.content else {}
    
    # ==================== CT-e ====================
    
    def emitir_cte(self, ref, dados_cte):
        """
        Emite um CT-e
        
        Args:
            ref: Referência única do CT-e (ex: 'cte_12345')
            dados_cte: Dicionário com dados do CT-e
        
        Returns:
            dict: Resposta da API
        """
        return self._request('POST', f'/v2/cte?ref={ref}', dados_cte)
    
    def consultar_cte(self, ref):
        """Consulta status de um CT-e"""
        return self._request('GET', f'/v2/cte/{ref}')
    
    def cancelar_cte(self, ref, justificativa):
        """Cancela um CT-e autorizado"""
        return self._request('DELETE', f'/v2/cte/{ref}', {'justificativa': justificativa})
    
    def carta_correcao_cte(self, ref, correcao):
        """Emite carta de correção para CT-e"""
        return self._request('POST', f'/v2/cte/{ref}/carta_correcao', {'correcao': correcao})
    
    # ==================== MDF-e ====================
    
    def emitir_mdfe(self, ref, dados_mdfe):
        """Emite um MDF-e"""
        return self._request('POST', f'/v2/mdfe?ref={ref}', dados_mdfe)
    
    def consultar_mdfe(self, ref):
        """Consulta status de um MDF-e"""
        return self._request('GET', f'/v2/mdfe/{ref}')
    
    def encerrar_mdfe(self, ref, dados_encerramento):
        """Encerra um MDF-e"""
        return self._request('POST', f'/v2/mdfe/{ref}/encerramento', dados_encerramento)
    
    def cancelar_mdfe(self, ref, justificativa):
        """Cancela um MDF-e"""
        return self._request('DELETE', f'/v2/mdfe/{ref}', {'justificativa': justificativa})


class CTeService:
    """Serviço para emissão de CT-e"""
    
    def __init__(self, tenant):
        self.tenant = tenant
        self.client = FocusNFeClient()
    
    def montar_cte(self, pedido):
        """Monta payload do CT-e a partir do pedido de frete"""
        from apps.clientes.models import Cliente
        
        cliente = pedido.cliente
        
        return {
            'natureza_operacao': 'PRESTACAO DE SERVICO DE TRANSPORTE',
            'tipo_servico': 0,  # Normal
            'cfop': '5353',  # Prestação de serviço de transporte
            'modal': 'rodoviario',
            
            # Emitente (dados do tenant)
            'cnpj_emitente': self.tenant.cnpj,
            'inscricao_estadual_emitente': self.tenant.inscricao_estadual or '',
            
            # Tomador
            'tipo_tomador': 0,  # Remetente
            'cnpj_tomador': cliente.cnpj,
            'inscricao_estadual_tomador': cliente.inscricao_estadual or '',
            'nome_tomador': cliente.razao_social,
            'logradouro_tomador': cliente.logradouro or '',
            'numero_tomador': cliente.numero or 'S/N',
            'bairro_tomador': cliente.bairro or '',
            'municipio_tomador': cliente.cidade or '',
            'uf_tomador': cliente.uf or '',
            'cep_tomador': (cliente.cep or '').replace('-', ''),
            
            # Remetente (mesmo que tomador)
            'cnpj_remetente': cliente.cnpj,
            'nome_remetente': cliente.razao_social,
            'municipio_remetente': pedido.origem_cidade,
            'uf_remetente': pedido.origem_uf,
            
            # Destinatário
            'cnpj_destinatario': cliente.cnpj,  # TODO: campo específico
            'nome_destinatario': cliente.razao_social,
            'municipio_destinatario': pedido.destino_cidade,
            'uf_destinatario': pedido.destino_uf,
            
            # Carga
            'valor_carga': float(pedido.valor_mercadoria or 0),
            'produto_predominante': pedido.tipo_carga,
            'quantidade_carga': float(pedido.peso_kg or 0),
            'unidade_carga': 'KG',
            
            # Valores
            'valor_total': float(pedido.valor_total),
            'valor_receber': float(pedido.valor_total),
            
            # Informações adicionais
            'informacoes_adicionais_fisco': f'Pedido: {pedido.numero}',
        }
    
    def emitir(self, cte_obj):
        """Emite CT-e via API Focus NFe"""
        from .models import CTe
        
        ref = f'cte_{cte_obj.id}'
        dados = self.montar_cte(cte_obj.pedido)
        
        cte_obj.status = 'processando'
        cte_obj.focusnfe_ref = ref
        cte_obj.save()
        
        try:
            response = self.client.emitir_cte(ref, dados)
            
            if response.get('status') == 'autorizado':
                cte_obj.status = 'autorizado'
                cte_obj.chave = response.get('chave_cte', '')
                cte_obj.protocolo = response.get('protocolo', '')
                cte_obj.numero = response.get('numero', '')
                cte_obj.data_autorizacao = timezone.now()
                cte_obj.pdf_url = response.get('caminho_danfe', '')
            elif response.get('status') == 'erro_autorizacao':
                cte_obj.status = 'rejeitado'
                cte_obj.mensagem_erro = response.get('mensagem', '')
            else:
                cte_obj.focusnfe_id = response.get('id', '')
            
            cte_obj.save()
            return response
            
        except Exception as e:
            cte_obj.status = 'rejeitado'
            cte_obj.mensagem_erro = str(e)
            cte_obj.save()
            raise
    
    def consultar(self, cte_obj):
        """Consulta status do CT-e"""
        if not cte_obj.focusnfe_ref:
            return None
        
        response = self.client.consultar_cte(cte_obj.focusnfe_ref)
        
        if response.get('status') == 'autorizado':
            cte_obj.status = 'autorizado'
            cte_obj.chave = response.get('chave_cte', '')
            cte_obj.protocolo = response.get('protocolo', '')
            cte_obj.pdf_url = response.get('caminho_danfe', '')
            cte_obj.save()
        
        return response
    
    def cancelar(self, cte_obj, justificativa):
        """Cancela CT-e autorizado"""
        if cte_obj.status != 'autorizado':
            raise ValueError('Apenas CT-e autorizado pode ser cancelado')
        
        response = self.client.cancelar_cte(cte_obj.focusnfe_ref, justificativa)
        
        if response.get('status') == 'cancelado':
            cte_obj.status = 'cancelado'
            cte_obj.save()
        
        return response


class MDFeService:
    """Serviço para emissão de MDF-e"""
    
    def __init__(self, tenant):
        self.tenant = tenant
        self.client = FocusNFeClient()
    
    def montar_mdfe(self, mdfe_obj):
        """Monta payload do MDF-e"""
        return {
            'uf_inicio': mdfe_obj.uf_inicio,
            'uf_fim': mdfe_obj.uf_fim,
            'cnpj_emitente': self.tenant.cnpj,
            'inscricao_estadual_emitente': self.tenant.inscricao_estadual or '',
            
            # Veículo
            'placa': mdfe_obj.veiculo.placa,
            'renavam': mdfe_obj.veiculo.renavam or '',
            'uf_licenciamento': mdfe_obj.veiculo.uf_licenciamento or mdfe_obj.uf_inicio,
            'tipo_rodado': '02',  # Truck
            'tipo_carroceria': '00',  # Não aplicável
            
            # Motorista
            'cpf_condutor': mdfe_obj.motorista.cpf,
            'nome_condutor': mdfe_obj.motorista.nome,
            
            # CT-es vinculados
            'documentos': [
                {'chave_cte': cte.chave}
                for cte in mdfe_obj.ctes.filter(status='autorizado')
            ],
        }
    
    def emitir(self, mdfe_obj):
        """Emite MDF-e via API"""
        ref = f'mdfe_{mdfe_obj.id}'
        dados = self.montar_mdfe(mdfe_obj)
        
        mdfe_obj.status = 'processando'
        mdfe_obj.focusnfe_ref = ref
        mdfe_obj.save()
        
        try:
            response = self.client.emitir_mdfe(ref, dados)
            
            if response.get('status') == 'autorizado':
                mdfe_obj.status = 'autorizado'
                mdfe_obj.chave = response.get('chave_mdfe', '')
                mdfe_obj.protocolo = response.get('protocolo', '')
                mdfe_obj.numero = response.get('numero', '')
                mdfe_obj.data_autorizacao = timezone.now()
                mdfe_obj.pdf_url = response.get('caminho_damdfe', '')
            
            mdfe_obj.save()
            return response
            
        except Exception as e:
            mdfe_obj.status = 'rejeitado'
            mdfe_obj.mensagem_erro = str(e)
            mdfe_obj.save()
            raise
    
    def encerrar(self, mdfe_obj, uf_encerramento, municipio_encerramento):
        """Encerra MDF-e"""
        if mdfe_obj.status != 'autorizado':
            raise ValueError('Apenas MDF-e autorizado pode ser encerrado')
        
        dados = {
            'uf': uf_encerramento,
            'codigo_municipio': municipio_encerramento,
        }
        
        response = self.client.encerrar_mdfe(mdfe_obj.focusnfe_ref, dados)
        
        if response.get('status') == 'encerrado':
            mdfe_obj.status = 'encerrado'
            mdfe_obj.data_encerramento = timezone.now()
            mdfe_obj.save()
        
        return response
