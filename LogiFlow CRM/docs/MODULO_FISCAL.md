# Módulo Fiscal - Emissão de CT-e/MDF-e Integrada

## 📋 Visão Geral

O Módulo Fiscal do LogiFlow CRM oferece uma solução completa para emissão, gestão e controle de documentos fiscais eletrônicos (CT-e e MDF-e) integrada diretamente ao sistema de gestão de transportes.

## ⚠️ IMPORTANTE - Focus NFe

**A Focus NFe é uma API PAGA e EXTERNA ao LogiFlow CRM.**

- ✅ LogiFlow oferece a **integração técnica**
- ❌ LogiFlow **NÃO fornece** chave de API
- 👤 **Cada cliente** deve contratar e configurar seu próprio token
- 💰 **Custos da Focus NFe** são de responsabilidade do cliente
- 🔑 **Token é armazenado** de forma segura por tenant (multi-tenancy)

**Como funciona:**
1. Cliente contrata Focus NFe (https://focusnfe.com.br)
2. Cliente obtém Token de API no painel Focus NFe
3. Cliente configura o Token no LogiFlow CRM
4. LogiFlow usa o Token do cliente para emitir documentos

---

## 🎯 Funcionalidades Implementadas

### ✅ Backend

#### Models de Persistência
- **CTe**: Model completo para armazenar CT-es com todos os campos necessários
- **MDFe**: Model completo para armazenar MDF-es com relacionamentos
- **ConfiguracaoFiscal**: Configurações fiscais por tenant (multi-tenancy)

#### Endpoints da API

**CT-e**
- `POST /fiscal/cte/emitir` - Emitir novo CT-e
- `GET /fiscal/cte` - Listar CT-es com filtros (status, data, pedido)
- `GET /fiscal/cte/{ref}` - Consultar CT-e específico
- `DELETE /fiscal/cte/{ref}` - Cancelar CT-e
- `GET /fiscal/cte/{ref}/pdf` - Download DACTE (PDF)
- `GET /fiscal/cte/{ref}/xml` - Download XML do CT-e

**MDF-e**
- `POST /fiscal/mdfe/emitir` - Emitir novo MDF-e
- `GET /fiscal/mdfe` - Listar MDF-es com filtros
- `GET /fiscal/mdfe/{ref}` - Consultar MDF-e específico
- `PATCH /fiscal/mdfe/{ref}/encerrar` - Encerrar MDF-e
- `DELETE /fiscal/mdfe/{ref}` - Cancelar MDF-e
- `GET /fiscal/mdfe/{ref}/pdf` - Download DAMDFE (PDF)
- `GET /fiscal/mdfe/{ref}/xml` - Download XML do MDF-e

**Configurações**
- `GET /fiscal/configuracao` - Obter configuração fiscal
- `POST /fiscal/configuracao` - Criar/atualizar configuração
- `PUT /fiscal/configuracao` - Atualizar configuração

**Dashboard**
- `GET /fiscal/dashboard` - Estatísticas fiscais (por mês/ano)

**Webhook**
- `POST /fiscal/webhook` - Receber notificações Focus NFe

#### Serviços

1. **FiscalService** (`backend/services/fiscal_service.py`)
   - Salvar CT-e e MDF-e no banco
   - Obter próximos números
   - Validar dados antes de emissão
   - Agrupar CT-es para MDF-e
   - Vincular CT-es ao MDF-e

2. **CRMSyncService** (`backend/services/crm_sync_service.py`)
   - Sincronizar CT-e com CRM Enterprise
   - Sincronizar MDF-e com CRM Enterprise
   - Atualizar status de pedidos

3. **NotificationService** (`backend/services/notification_service.py`)
   - Enviar email com CT-e/MDF-e
   - Enviar WhatsApp com CT-e/MDF-e
   - Notificações automáticas após emissão

#### Integração Focus NFe

Cliente completo (`backend/integrations/fiscal/focusnfe.py`) com:
- Emitir CT-e
- Emitir MDF-e
- Consultar documentos
- Cancelar documentos
- Encerrar MDF-e
- Download de PDF e XML

### ✅ Frontend

#### Views Criadas

1. **ListarCTeView.vue** - Lista de CT-es emitidos
   - Filtros por status, data, pedido
   - Paginação
   - Download PDF/XML
   - Cancelamento
   - Navegação para detalhes

2. **ListarMDFeView.vue** - Lista de MDF-es emitidos
   - Filtros por status e data
   - Paginação
   - Download PDF/XML
   - Encerramento e cancelamento
   - Navegação para detalhes

3. **EmitirCTeView.vue** - Formulário de emissão de CT-e
   - Preenchimento automático de dados do pedido
   - Validação de campos
   - Confirmação visual após emissão

4. **EmitirMDFeView.vue** - Formulário de emissão de MDF-e
   - Seleção de CT-es disponíveis
   - Totalizadores automáticos
   - Gestão de condutores
   - Percurso automático baseado em CT-es

5. **DetalhesCTeView.vue** - Detalhes completos do CT-e
   - Todas as informações do documento
   - Downloads
   - Status e histórico

6. **DetalhesMDFeView.vue** - Detalhes completos do MDF-e
   - Todas as informações do documento
   - CT-es vinculados
   - Percurso e condutores

7. **ConfiguracoesFiscaisView.vue** - Configurações fiscais
   - Dados do emitente
   - Séries e numerações
   - Integração Focus NFe
   - RNTRC e ANTT
   - Configurações de emissão automática
   - Notificações

8. **DashboardFiscalView.vue** - Dashboard com estatísticas
   - Total de CT-es e MDF-es
   - Valores totais
   - Gráficos por status
   - Taxa de sucesso
   - Ações rápidas

#### Rotas Configuradas

```javascript
{ path: 'fiscal/cte', name: 'ListarCTe' }
{ path: 'fiscal/cte/:ref', name: 'DetalhesCTe' }
{ path: 'fiscal/mdfe', name: 'ListarMDFe' }
{ path: 'fiscal/mdfe/emitir', name: 'EmitirMDFe' }
{ path: 'fiscal/mdfe/:ref', name: 'DetalhesMDFe' }
{ path: 'fiscal/dashboard', name: 'DashboardFiscal' }
{ path: 'configuracoes/fiscal', name: 'ConfiguracoesFiscais' }
{ path: 'pedidos/:id/emitir-cte', name: 'EmitirCTe' }
```

## 🚀 Como Usar

### 1. Configuração Inicial

#### Backend - Criar Tabelas no Banco

As tabelas serão criadas automaticamente ao iniciar a aplicação:

```bash
# Reiniciar o backend para criar as tabelas
python main.py
```

> **⚠️ IMPORTANTE**: A Focus NFe é uma **API PAGA** que cada cliente deve contratar e configurar individualmente. O LogiFlow CRM apenas oferece a integração.

### 2. Cliente Configura Focus NFe

**Cada cliente precisa:**

1. **Contratar a Focus NFe**
   - Acessar: https://focusnfe.com.br
   - Criar conta e contratar plano
   - Obter Token de API no painel Focus NFe

2. **Configurar no LogiFlow**
   - Acessar **Configurações > Configurações Fiscais**
   - Preencher dados do emitente (CNPJ, Razão Social, IE, Endereço)
   - **Colar o Token Focus NFe** (obtido no passo 1)
   - Selecionar ambiente (Homologação ou Produção)
   - Configurar RNTRC e ANTT (se aplicável)
   - Definir séries padrão para CT-e e MDF-e
   - Configurar preferências de emissão automática

> 💡 **Dica**: Comece sempre no ambiente de **Homologação** para testes antes de ir para Produção.

### 3. Emitir CT-e

#### Opção 1: A partir de um Pedido
1. Acesse **Pedidos**
2. Clique no pedido desejado
3. Clique em **Emitir CT-e**
4. Revise os dados pré-preenchidos
5. Clique em **Emitir CT-e**

#### Opção 2: Diretamente
1. Acesse **Fiscal > CT-es**
2. Clique em **Emitir CT-e**
3. Preencha todos os dados
4. Clique em **Emitir CT-e**

### 4. Emitir MDF-e

1. Acesse **Fiscal > MDF-es**
2. Clique em **Emitir MDF-e**
3. Selecione os CT-es que serão incluídos
4. Preencha dados do veículo e condutores
5. Revise o percurso automático
6. Clique em **Emitir MDF-e**

### 5. Gerenciar Documentos

#### Listar e Filtrar
- Acesse **Fiscal > CT-es** ou **Fiscal > MDF-es**
- Use os filtros por status, data, etc.
- Clique em qualquer documento para ver detalhes

#### Download de Documentos
- Na listagem ou detalhes, clique em **Baixar PDF** ou **Baixar XML**

#### Cancelar Documentos
- Somente documentos autorizados podem ser cancelados
- Clique em **Cancelar**
- Informe justificativa (mínimo 15 caracteres)
- Confirme o cancelamento

#### Encerrar MDF-e
- Somente MDF-es autorizados podem ser encerrados
- Clique em **Encerrar**
- Informe UF e código IBGE da cidade
- Confirme o encerramento

### 6. Dashboard Fiscal

Acesse **Fiscal > Dashboard** para visualizar:
- Total de documentos emitidos no período
- Valores totais
- Distribuição por status
- Taxa de sucesso
- Ações rápidas

## 🔧 Configurações Avançadas

### Emissão Automática

No painel de configurações fiscais, você pode habilitar:

- **Emitir CT-e automaticamente**: CT-e será emitido ao aprovar pedido
- **Agrupar em MDF-e automaticamente**: CT-es serão agrupados automaticamente
- **Enviar email após emissão**: Cliente receberá email com DACTE
- **Enviar WhatsApp após emissão**: Cliente receberá mensagem no WhatsApp

### Validações

Configure validações obrigatórias:
- **Validar dados antes de emissão**: Verifica integridade dos dados
- **Exigir RNTRC**: Torna RNTRC obrigatório
- **Exigir CIOT**: Torna CIOT obrigatório

### Observações Padrão

Configure observações que aparecerão automaticamente em:
- Todos os CT-es
- Todos os MDF-es

### Webhook Focus NFe

Configure o webhook no painel Focus NFe apontando para:
```
https://seu-dominio.com/api/v1/fiscal/webhook
```

O sistema atualizará automaticamente o status dos documentos.

## 📊 Fluxo Completo de Trabalho

```
1. Cliente solicita frete
   ↓
2. Pedido criado no sistema
   ↓
3. Pedido aprovado
   ↓
4. CT-e emitido (manual ou automático)
   ↓
5. CT-e autorizado pela SEFAZ
   ↓
6. Cliente notificado (email/WhatsApp)
   ↓
7. CT-es agrupados em MDF-e
   ↓
8. MDF-e autorizado pela SEFAZ
   ↓
9. Transporte realizado
   ↓
10. MDF-e encerrado
```

## 🔐 Segurança

- ✅ Multi-tenancy: Cada tenant tem seus próprios documentos
- ✅ Autenticação: Todos os endpoints requerem autenticação
- ✅ Validação: Dados validados antes de envio à SEFAZ
- ✅ Auditoria: Todas as ações são registradas com timestamp
- ✅ Token seguro: Token Focus NFe armazenado de forma segura

## 📈 Performance

- ✅ Paginação: Listas paginadas para melhor performance
- ✅ Filtros: Busca otimizada com índices no banco
- ✅ Cache: Configurações em cache para reduzir consultas
- ✅ Async: Operações assíncronas onde possível

## 🐛 Troubleshooting

### CT-e rejeitado pela SEFAZ

1. Verifique os dados do emitente nas configurações
2. Confirme que o certificado digital está válido
3. Revise os dados do documento (CNPJ, IE, valores)
4. Consulte o motivo da rejeição nos detalhes do CT-e

### Focus NFe retorna erro 401

1. **Verifique o token do cliente** nas Configurações Fiscais
2. Confirme que o token está correto (copie novamente do painel Focus NFe)
3. Verifique se o cliente tem saldo/créditos na Focus NFe
4. Confirme que o token não expirou
5. Teste o token diretamente no painel Focus NFe

> 💡 Cada cliente tem seu próprio token Focus NFe. Não há token global da plataforma.

### Não consigo cancelar CT-e

1. CT-e deve estar com status "autorizado"
2. Justificativa deve ter no mínimo 15 caracteres
3. Verifique se há prazo limite para cancelamento

### MDF-e não encerra

1. Certifique-se de que o MDF-e está autorizado
2. Código IBGE deve estar correto (7 dígitos)
3. UF de encerramento deve fazer parte do percurso

## 📚 Referências

- [Manual Focus NFe](https://focusnfe.com.br/doc/)
- [Manual CT-e SEFAZ](http://www.cte.fazenda.gov.br/)
- [Manual MDF-e SEFAZ](http://www.mdfe.fazenda.gov.br/)

## 🎉 Recursos Futuros

Próximas implementações planejadas:
- ❌ Inutilização de numeração de CT-e/MDF-e
- ❌ Carta de Correção Eletrônica (CC-e)
- ❌ Contingência (emissão offline)
- ❌ Relatórios avançados de faturamento
- ❌ Exportação de dados para Excel
- ❌ Dashboard com gráficos interativos

## 📝 Notas Importantes

1. **Ambiente de Homologação**: Sempre teste primeiro em homologação
2. **Certificado Digital**: Necessário para ambiente de produção
3. **Credenciamento SEFAZ**: Empresa deve estar credenciada na SEFAZ
4. **Numeração Sequencial**: CT-e e MDF-e devem ter numeração sequencial por série
5. **Backup**: Faça backup regular dos XMLs autorizados

## 💡 Dicas

- Configure atalhos no menu lateral para acesso rápido
- Use o dashboard fiscal como página inicial do módulo
- Configure notificações automáticas para economizar tempo
- Mantenha sempre backup dos XMLs e PDFs
- Revise periodicamente as configurações fiscais

## 🤝 Suporte

Para dúvidas ou problemas:
1. Consulte esta documentação
2. Verifique os logs do sistema
3. Entre em contato com o suporte técnico

---

**Versão**: 1.0.0  
**Data**: Janeiro 2026  
**Desenvolvido por**: LogiFlow CRM Team
