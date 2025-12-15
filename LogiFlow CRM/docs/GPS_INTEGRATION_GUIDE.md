# 🛰️ Guia de Integração GPS - Sascar, Autotrac, Onixsat

## 📋 Status das Integrações

| Provider | Status | Documentação | Necessário |
|----------|--------|--------------|------------|
| Sascar | ⚠️ Template | Privada (B2B) | Credenciais + Docs |
| Autotrac | ⚠️ Template | Privada (B2B) | Credenciais + Docs |
| Onixsat | ⚠️ Template | Privada (B2B) | Credenciais + Docs |

---

## 🎯 Situação Atual

### ✅ O que JÁ ESTÁ implementado:
1. **Infraestrutura completa** de multi-tenancy
2. **Sistema de credenciais** criptografadas no banco
3. **Endpoints consolidados** que agregam dados de múltiplos providers
4. **Frontend** com telas de GPS e configuração
5. **Templates das integrações** prontos para adaptar

### ⚠️ O que FALTA:
1. **Documentação oficial** das APIs (Sascar, Autotrac, Onixsat)
2. **Credenciais de teste/produção** para validar
3. **Ajustar os templates** com os endpoints e formatos reais

---

## 📞 Como Obter as Documentações

### 1. **Sascar**
- **Site**: https://www.sascar.com.br
- **Contato**: Solicitar à equipe comercial/suporte técnico
- **Perguntar por**: 
  - "Documentação da API REST para integração"
  - "Manual de integração de sistemas"
  - "Credenciais de ambiente sandbox/homologação"

**O que você precisa**:
- Base URL da API (ex: `https://api.sascar.com.br/v1`)
- Método de autenticação (API Key? OAuth? Bearer Token?)
- Endpoints disponíveis:
  - Listar veículos
  - Obter posição atual
  - Obter histórico de rota
  - Webhook para posições em tempo real (se disponível)
- Formato das respostas (JSON? XML?)

---

### 2. **Autotrac**
- **Site**: https://www.autotrac.com.br
- **Contato**: Solicitar à equipe de integrações
- **Perguntar por**:
  - "API de integração para rastreamento"
  - "Documentação técnica para desenvolvedores"
  - "Ambiente de testes (sandbox)"

**O que você precisa**:
- Base URL (ex: `https://api.autotrac.com.br/v2`)
- Autenticação (Username/Password? Token?)
- Endpoints:
  - `/veiculos` - Listar veículos
  - `/veiculos/{id}/posicao` - Posição atual
  - `/veiculos/{id}/historico` - Histórico
  - Webhooks (se houver)
- Exemplos de requisições e respostas

---

### 3. **Onixsat**
- **Site**: https://www.onixsat.com.br
- **Contato**: Suporte técnico ou comercial
- **Perguntar por**:
  - "API REST para integração de sistemas"
  - "Manual do desenvolvedor"
  - "Credenciais de homologação"

**O que você precisa**:
- Base URL (ex: `https://api.onixsat.com.br`)
- Token de autenticação
- Endpoints:
  - Listar dispositivos/veículos
  - Posição em tempo real
  - Histórico de trajeto
  - Alertas/eventos
- Formato de datas (ISO 8601? Unix timestamp?)

---

## 🔧 Como Adaptar os Templates

Quando você conseguir a documentação, siga estes passos:

### **Passo 1: Obter Credenciais de Teste**

Peça ao provider:
- Credenciais de ambiente **sandbox/homologação**
- Alguns veículos de teste já cadastrados
- Placa de exemplo para testar

### **Passo 2: Testar Manualmente (Postman/cURL)**

Antes de alterar o código, teste a API manualmente:

```bash
# Exemplo genérico (ajustar conforme documentação):
curl -X GET "https://api.sascar.com.br/v1/veiculos" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json"
```

Anote:
- Se funcionou
- Formato da resposta
- Campos importantes (lat, lng, velocidade, timestamp, etc.)

### **Passo 3: Atualizar o Código**

Edite o arquivo do provider (ex: `backend/integrations/gps/sascar.py`):

**3.1. Ajustar a Base URL**
```python
BASE_URL = "https://api.sascar.com.br/v1"  # URL real da documentação
```

**3.2. Ajustar autenticação**
```python
def _get_headers(self):
    return {
        "Authorization": f"Bearer {self.api_key}",  # Ou o formato correto
        "Content-Type": "application/json"
    }
```

**3.3. Ajustar os endpoints**
```python
def obter_posicao_veiculo(self, placa: str):
    # Usar o endpoint real da documentação:
    response = requests.get(
        f"{self.BASE_URL}/veiculos/{placa}/posicao",  # Endpoint real
        headers=self._get_headers(),
        timeout=10
    )
```

**3.4. Mapear a resposta**
```python
# Adaptar campos da resposta para o formato LogiFlow:
return {
    "success": True,
    "placa": placa,
    "posicao": {
        "latitude": data["lat"],        # Ajustar nome do campo
        "longitude": data["lon"],       # Ajustar nome do campo
        "velocidade": data["speed"],    # Ajustar nome do campo
        "data_hora": data["timestamp"], # Ajustar nome do campo
        # ... outros campos
    }
}
```

### **Passo 4: Testar com Credenciais Reais**

```bash
cd "LogiFlow CRM/backend"
python scripts/test_gps_provider.py sascar
```

### **Passo 5: Cadastrar no Sistema**

Via interface web ou API:
```json
POST /api/v1/tenant-credentials/credentials
{
  "integration_type": "gps",
  "provider": "sascar",
  "credentials": {
    "api_key": "sua_chave_aqui",
    "api_secret": "seu_secret_aqui",
    "environment": "production"
  }
}
```

---

## 📝 Template de E-mail para Solicitar Documentação

```
Assunto: Solicitação de Documentação da API de Integração

Prezados,

Somos a empresa [SUA EMPRESA] e utilizamos os serviços de rastreamento 
da [SASCAR/AUTOTRAC/ONIXSAT].

Estamos desenvolvendo uma integração automatizada entre nosso sistema 
de gestão logística (LogiFlow CRM) e a plataforma de rastreamento, 
e gostaríamos de solicitar:

1. Documentação técnica da API REST para integração
2. Especificação dos endpoints disponíveis
3. Exemplos de requisições e respostas
4. Credenciais de ambiente de homologação/testes
5. Suporte técnico durante a implementação (se disponível)

Nosso objetivo é automatizar:
- Consulta de posições de veículos em tempo real
- Listagem de frota rastreada
- Histórico de rotas/trajetos
- Recebimento de webhooks (se disponível)

Aguardamos retorno.

Atenciosamente,
[SEU NOME]
[SUA EMPRESA]
[SEU CONTATO]
```

---

## 🔍 Informações Comuns em APIs de GPS

Baseado em padrões do mercado, as APIs geralmente têm:

### **Autenticação**
- API Key + Secret
- Bearer Token
- OAuth 2.0
- Basic Auth (username/password)

### **Endpoints Típicos**
```
GET  /veiculos                    - Lista todos os veículos
GET  /veiculos/{id}               - Detalhes de um veículo
GET  /veiculos/{id}/posicao       - Posição atual
GET  /veiculos/{id}/historico     - Histórico de rotas
GET  /veiculos/{id}/alertas       - Alertas/eventos
POST /webhooks                    - Configurar webhook
```

### **Formato de Posição**
```json
{
  "veiculo_id": "123",
  "placa": "ABC1234",
  "latitude": -23.5505,
  "longitude": -46.6333,
  "velocidade": 60,
  "ignicao": true,
  "data_hora": "2025-12-15T14:30:00Z",
  "odometro": 123456,
  "status": "em_movimento"
}
```

---

## 🚀 Próximos Passos

1. ✅ **Infraestrutura está pronta**
2. ⏳ **Você solicita a documentação aos providers**
3. ⏳ **Recebe credenciais de teste**
4. ⏳ **Testa manualmente (Postman)**
5. ⏳ **Me envia exemplos de respostas**
6. ✅ **Eu adapto os templates**
7. ✅ **Testamos juntos**
8. ✅ **Deploy em produção**

---

## 💡 Alternativas Enquanto Aguarda

Se demorar para conseguir as documentações:

### **Opção 1: Usar Modo Simulação** ✅
- Já implementado
- Frontend funciona normalmente
- Dados fictícios para demonstração
- Pode fazer MVP/testes de UX

### **Opção 2: Webhooks Genéricos** ✅
- Criar endpoint que recebe qualquer JSON
- Logar tudo que chegar
- Analisar formato depois
- Adaptar conforme necessário

### **Opção 3: APIs Alternativas** 
- GPS-Trace (tem API pública)
- Traccar (open source)
- Usar temporariamente até conseguir as principais

---

## 📞 Precisa de Ajuda?

Quando conseguir a documentação:
1. **Me envie**: Exemplos de respostas JSON
2. **Eu adapto**: O código em minutos
3. **Testamos**: Juntos com suas credenciais

---

**O sistema está 100% preparado para receber as integrações reais!** 🚀

Só precisamos dos detalhes técnicos dos providers.

