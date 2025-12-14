# 📚 Base de Conhecimento LogiFlow CRM

Bem-vindo à Base de Conhecimento do LogiFlow CRM! Aqui você encontra toda a documentação necessária para usar o sistema.

---

## 🚀 Início Rápido

### Primeiros Passos
1. [Guia de Início Rápido](GUIA_INICIO_RAPIDO.md)
2. [Instalação e Configuração](SUITECRM_INSTALL.md)
3. [FAQ - Perguntas Frequentes](../frontend/src/views/FAQView.vue)

---

## 📖 Documentação dos Módulos

### Gestão de Clientes
- [Módulo Clientes](../backend/docs/MODULO_CLIENTES.md)
  - Cadastro de clientes
  - Gestão de relacionamento
  - Histórico de interações
  - Integrações ERP

### Cotações e Pedidos
- [Módulo Cotações](../backend/docs/MODULO_COTACOES.md)
  - Criar cotações
  - Cálculo automático de frete
  - Integração Melhor Envio e Frenet
  - Converter em pedido

- [Módulo Pedidos](../backend/docs/MODULO_PEDIDOS.md)
  - Gestão de pedidos
  - Emissão de CT-e
  - Rastreamento
  - Comprovantes de entrega

### Entregas
- [Módulo Entregas](../backend/docs/MODULO_ENTREGAS.md)
  - Rastreamento GPS
  - Comprovantes digitais
  - Portal do cliente
  - App do motorista

### Comunicação
- [Módulo WhatsApp](../backend/docs/MODULO_WHATSAPP.md)
  - Configuração Evolution API
  - Templates de mensagens
  - Notificações automáticas
  - Histórico de conversas

---

## 🔧 Integrações

### Integrações ERP
- [Omie e Bling](../backend/docs/INTEGRACOES_ERP.md)
  - Sincronização de clientes
  - Sincronização de pedidos
  - Geração de faturas

### Cotação de Frete
- [Melhor Envio](../backend/docs/MELHOR_ENVIO.md)
  - Cotação automática
  - Múltiplas transportadoras
  - Rastreamento

### Documentos Fiscais
- Emissão de CT-e
- Emissão de MDF-e
- Consulta e cancelamento
- Download de documentos

---

## 📊 Glossário de Termos

- [Glossário Completo](../backend/docs/GLOSSARIO.md)
  - Termos técnicos
  - Siglas e abreviações
  - Conceitos de logística

---

## 🎓 Tutoriais

### Vídeos de Treinamento
1. Visão Geral do Sistema (5min)
2. Cadastro de Clientes (8min)
3. Criando Cotações (10min)
4. Convertendo Cotação em Pedido (5min)
5. Acompanhando Entregas (8min)
6. Usando o Dashboard (5min)
7. App do Motorista (8min)
8. Emitindo CT-e (10min)

### Guias Passo a Passo
- Como criar uma cotação
- Como emitir um CT-e
- Como rastrear uma entrega
- Como configurar WhatsApp
- Como migrar dados

---

## 🔍 Busca Rápida

### Por Funcionalidade
- **Cadastros:** Clientes, Motoristas, Veículos
- **Operacional:** Cotações, Pedidos, Entregas
- **Fiscal:** CT-e, MDF-e, Notas Fiscais
- **Comunicação:** WhatsApp, Email, Notificações
- **Relatórios:** Dashboard, Análises, Exportações

### Por Problema
- [Troubleshooting Comum](#troubleshooting)
- [Erros Frequentes](#erros-frequentes)
- [Dúvidas Técnicas](#duvidas-tecnicas)

---

## 📞 Suporte

### Canais de Atendimento
- **Email:** suporte@logiflow.com.br
- **WhatsApp:** (11) 99999-9999
- **Horário:** Segunda a Sexta, 8h às 18h

### Níveis de Suporte
- **Nível 1:** Dúvidas gerais e orientações
- **Nível 2:** Problemas técnicos e configurações
- **Nível 3:** Bugs e desenvolvimento

---

## 🔄 Atualizações

### Versão Atual: 1.0.0
**Data:** 14 de Dezembro de 2024

**Últimas Atualizações:**
- ✅ Sistema de Health Score e Customer Success
- ✅ Sistema de NPS e Satisfação
- ✅ Integração Frenet
- ✅ Cotação Automática Consolidada
- ✅ Tela de Emissão CT-e
- ✅ 6 Documentações de Módulos

### Histórico de Versões
- **1.0.0** (14/12/2024) - Lançamento oficial
- **0.9.0** (10/12/2024) - Beta público
- **0.8.0** (05/12/2024) - Alpha interno

---

## 📋 Índice Completo

### A
- [Alertas de Churn](../backend/docs/HEALTH_SCORE_IMPLEMENTADO.md)
- [API Documentation](../backend/docs/)
- [Autenticação](../backend/routers/auth.py)

### C
- [Clientes](../backend/docs/MODULO_CLIENTES.md)
- [Cotações](../backend/docs/MODULO_COTACOES.md)
- [CT-e](../frontend/README_CTE.md)
- [Customer Success](../HEALTH_SCORE_IMPLEMENTADO.md)

### D
- [Dashboard](../frontend/src/views/DashboardView.vue)
- [Documentação](../backend/docs/)

### E
- [Entregas](../backend/docs/MODULO_ENTREGAS.md)
- [ERP](../backend/docs/INTEGRACOES_ERP.md)

### F
- [FAQ](../frontend/src/views/FAQView.vue)
- [Frenet](../backend/integrations/frete/frenet.py)

### G
- [Glossário](../backend/docs/GLOSSARIO.md)
- [Google Maps](../backend/routers/maps.py)

### H
- [Health Score](../HEALTH_SCORE_IMPLEMENTADO.md)

### I
- [Integrações](../backend/docs/INTEGRACOES_ERP.md)
- [Instalação](SUITECRM_INSTALL.md)

### M
- [Melhor Envio](../backend/docs/MELHOR_ENVIO.md)
- [Migração de Dados](../backend/docs/GUIA_MIGRACAO_DADOS.md)

### N
- [NPS](../backend/services/nps_service.py)

### P
- [Pedidos](../backend/docs/MODULO_PEDIDOS.md)

### R
- [Rastreamento](../backend/routers/rastreamento.py)
- [Relatórios](../backend/docs/)

### W
- [WhatsApp](../backend/docs/MODULO_WHATSAPP.md)

---

## 🎯 Casos de Uso

### Transportadora Pequena (1-5 veículos)
- Foco em cotações e pedidos
- WhatsApp para comunicação
- Rastreamento básico

### Transportadora Média (6-20 veículos)
- Integração com ERP
- Emissão de CT-e
- Dashboard de performance

### Transportadora Grande (20+ veículos)
- Health Score e CS
- NPS e satisfação
- Múltiplas integrações

---

## 💡 Dicas e Truques

### Atalhos de Teclado
- `Ctrl + N` - Novo registro
- `Ctrl + S` - Salvar
- `Ctrl + F` - Buscar
- `Esc` - Cancelar

### Melhores Práticas
1. Sempre preencher dados completos
2. Usar cotação automática
3. Emitir CT-e antes do transporte
4. Manter cliente informado via WhatsApp
5. Registrar todas as ocorrências

---

## 🔐 Segurança

### Boas Práticas
- Usar senhas fortes
- Ativar autenticação de dois fatores
- Não compartilhar credenciais
- Fazer backup regular

### Privacidade
- Dados criptografados
- Conformidade LGPD
- Auditoria de acessos

---

## 📈 Roadmap

### Próximas Funcionalidades
- [ ] Google Distance Matrix
- [ ] Rastreamento GPS Avançado (Sascar, Autotrac)
- [ ] Machine Learning para predição
- [ ] App mobile nativo
- [ ] Chatbot com IA

---

## 🤝 Contribuindo

### Como Reportar Bugs
1. Descrever o problema
2. Passos para reproduzir
3. Screenshots se possível
4. Enviar para suporte@logiflow.com.br

### Sugestões de Melhorias
- Use o formulário de feedback
- Participe das pesquisas NPS
- Entre em contato com CS

---

## 📄 Licença

LogiFlow CRM - Todos os direitos reservados © 2024

---

**Desenvolvido com ❤️ para Transportadoras Brasileiras**

**Última atualização:** 14 de Dezembro de 2024
