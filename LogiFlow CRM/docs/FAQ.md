# ❓ FAQ - Perguntas Frequentes - LogiFlow CRM

## 📋 Índice
- [Geral](#geral)
- [Acesso e Login](#acesso-e-login)
- [Cadastros](#cadastros)
- [Cotações e Pedidos](#cotações-e-pedidos)
- [Entregas](#entregas)
- [Fiscal (CT-e/MDF-e)](#fiscal-ct-e-mdf-e)
- [App do Motorista](#app-do-motorista)
- [Problemas Técnicos](#problemas-técnicos)
- [Planos e Pagamento](#planos-e-pagamento)

---

## Geral

### O que é o LogiFlow CRM?
O LogiFlow é um sistema completo de gestão para transportadoras que integra CRM comercial, TMS operacional e emissão de documentos fiscais em uma única plataforma.

### Quais funcionalidades estão incluídas?
- ✅ Gestão de clientes e cotações
- ✅ Controle de pedidos e entregas
- ✅ Rastreamento em tempo real
- ✅ App do motorista (PWA)
- ✅ Portal do cliente
- ✅ Emissão de CT-e/MDF-e
- ✅ Integração WhatsApp
- ✅ Relatórios e dashboards

### Preciso instalar algum software?
Não! O LogiFlow é 100% web. Basta acessar pelo navegador (Chrome, Firefox, Edge ou Safari).

### Funciona no celular?
Sim! O sistema é responsivo e funciona perfeitamente em smartphones e tablets.

---

## Acesso e Login

### Esqueci minha senha, o que fazer?
1. Na tela de login, clique em "Esqueci minha senha"
2. Digite seu e-mail cadastrado
3. Você receberá um link para redefinir a senha
4. Acesse o link e crie uma nova senha

### Posso ter múltiplos usuários?
Sim! O número de usuários depende do seu plano:
- **Starter**: Até 5 usuários
- **Professional**: Até 15 usuários
- **Enterprise**: Usuários ilimitados

### Como adicionar um novo usuário?
1. Menu → **Configurações** → **Usuários**
2. Clique em **Novo Usuário**
3. Preencha nome, e-mail e defina permissões
4. O usuário receberá um e-mail com instruções de acesso

### Posso definir permissões diferentes para cada usuário?
Sim! Você pode criar perfis personalizados:
- **Administrador**: Acesso total
- **Gerente**: Visualiza tudo, edita operação
- **Comercial**: Apenas cotações e clientes
- **Operacional**: Apenas pedidos e entregas
- **Motorista**: Apenas app do motorista

---

## Cadastros

### Como importar meus clientes do sistema antigo?
1. Baixe o template Excel em **Templates** → `template_clientes.xlsx`
2. Preencha com seus dados
3. Valide: `python scripts/validar_importacao.py --arquivo meus_clientes.xlsx --tipo clientes`
4. Importe: `python scripts/importar_dados.py --arquivo meus_clientes.xlsx --tipo clientes`

Ou solicite ajuda ao suporte para migração assistida.

### O sistema busca dados da Receita Federal automaticamente?
Sim! Ao cadastrar um cliente, digite o CNPJ e clique em "Buscar". O sistema preenche automaticamente:
- Razão social
- Nome fantasia
- Endereço
- Atividade principal

### Posso cadastrar clientes pessoa física?
Sim! Basta usar CPF em vez de CNPJ.

### Como cadastrar um veículo?
1. Menu → **Frota** → **Veículos** → **Novo**
2. Preencha placa, tipo, marca e modelo
3. Adicione dados opcionais (Renavam, capacidade, etc)
4. Associe a um motorista (opcional)
5. Salve

---

## Cotações e Pedidos

### Como criar uma cotação?
1. Menu → **Comercial** → **Nova Cotação**
2. Selecione o cliente
3. Preencha origem e destino (CEP ou cidade)
4. Informe tipo de carga, peso e volumes
5. Sistema calcula o valor automaticamente
6. Ajuste se necessário e envie

### O sistema calcula o frete automaticamente?
Sim! Baseado em:
- Distância (via Google Maps)
- Peso e volume da carga
- Tabela de preços configurada
- Pedágios e custos operacionais

Você pode ajustar o valor manualmente antes de enviar.

### Como converter uma cotação em pedido?
1. Abra a cotação aprovada
2. Clique em **Converter em Pedido**
3. Confirme os dados
4. Pedido é criado automaticamente
5. Você pode então programar a coleta

### Posso enviar a cotação por WhatsApp?
Sim! Ao criar a cotação, clique em **Enviar por WhatsApp**. O cliente recebe um link com todos os detalhes.

### Como cancelar um pedido?
1. Abra o pedido
2. Clique em **Ações** → **Cancelar**
3. Informe o motivo
4. Confirme

**Atenção**: Pedidos com CT-e emitido precisam ter o documento cancelado primeiro.

---

## Entregas

### Como acompanhar uma entrega em tempo real?
1. Menu → **Operacional** → **Entregas**
2. Clique na entrega desejada
3. Visualize o mapa com localização do motorista
4. Veja histórico de status

### O cliente pode rastrear a entrega?
Sim! Cada entrega tem um link público que pode ser compartilhado:
1. Abra a entrega
2. Clique em **Compartilhar Rastreamento**
3. Copie o link ou envie por WhatsApp
4. Cliente acessa sem precisar de login

### Como o motorista atualiza o status?
Pelo **App do Motorista**:
1. Motorista acessa app.logiflow.com.br
2. Faz login com CPF e senha
3. Vê suas entregas do dia
4. Atualiza status: Coletado → Em trânsito → Entregue
5. Pode tirar foto do comprovante

### O que fazer se houver uma ocorrência?
1. Abra a entrega
2. Clique em **Registrar Ocorrência**
3. Selecione o tipo (Atraso, Avaria, Recusa, etc)
4. Descreva o problema
5. Anexe fotos se necessário
6. Sistema notifica automaticamente o cliente

---

## Fiscal (CT-e/MDF-e)

### Como emitir um CT-e?
1. Abra o pedido
2. Clique em **Emitir CT-e**
3. Confira os dados (remetente, destinatário, valores)
4. Clique em **Transmitir**
5. Aguarde autorização da SEFAZ (1-2 minutos)
6. CT-e autorizado! Baixe XML e DACTE

### Preciso de certificado digital?
Sim, é obrigatório para emitir CT-e. Você pode:
- Usar certificado A1 (arquivo .pfx)
- Usar certificado A3 (token/cartão)

Configure em: **Configurações** → **Fiscal** → **Certificado Digital**

### Como cancelar um CT-e?
1. Abra o pedido com CT-e emitido
2. Clique em **Ações** → **Cancelar CT-e**
3. Informe o motivo (mínimo 15 caracteres)
4. Confirme

**Prazo**: Até 24h após emissão ou antes da entrega.

### O que é MDF-e e quando preciso emitir?
MDF-e (Manifesto de Documentos Fiscais) é obrigatório para:
- Transporte interestadual
- Mais de 1 CT-e no mesmo veículo

Emita em: **Operacional** → **MDF-e** → **Novo**

### Quanto custa a emissão de documentos?
Depende do provedor:
- **Focus NFe**: ~R$ 0,15 por documento
- **Webmania**: R$ 49-199/mês (ilimitado)

Já está incluído no seu plano LogiFlow.

---

## App do Motorista

### Como o motorista acessa o app?
1. Acesse **app.logiflow.com.br** pelo celular
2. Faça login com CPF e senha
3. Pronto! Não precisa instalar nada

### Funciona offline?
Sim! O app funciona offline e sincroniza quando houver internet.

### Como tirar foto do comprovante de entrega?
1. No app, abra a entrega
2. Clique em **Finalizar Entrega**
3. Toque em **Tirar Foto**
4. Fotografe o comprovante assinado
5. Confirme a entrega

A foto fica disponível no sistema para o cliente.

### Motorista pode recusar uma carga?
Sim, no app:
1. Veja a carga atribuída
2. Se não puder aceitar, clique em **Recusar**
3. Informe o motivo
4. Gestor é notificado e pode realocar

---

## Problemas Técnicos

### O sistema está lento, o que fazer?
1. Verifique sua conexão de internet
2. Limpe o cache do navegador (Ctrl+Shift+Del)
3. Tente outro navegador
4. Se persistir, contate o suporte

### Não consigo fazer login
Verifique:
- ✅ E-mail está correto (sem espaços)
- ✅ Senha está correta (maiúsculas/minúsculas)
- ✅ Caps Lock está desligado
- ✅ Não há problemas de conexão

Se não resolver, use "Esqueci minha senha".

### Erro ao emitir CT-e
Causas comuns:
- ❌ Certificado digital vencido ou inválido
- ❌ Dados incompletos (CFOP, natureza, etc)
- ❌ SEFAZ fora do ar
- ❌ Empresa sem autorização para emitir CT-e

Veja o erro específico e corrija. Se precisar de ajuda, contate o suporte.

### Como faço backup dos meus dados?
Os dados são automaticamente salvos em nuvem com backup diário. Você também pode exportar:
1. Menu → **Relatórios** → **Exportar Dados**
2. Selecione período e tipo de dados
3. Baixe o arquivo Excel/CSV

---

## Planos e Pagamento

### Quais são os planos disponíveis?
| Plano | Preço | Usuários | Veículos | Pedidos/mês |
|-------|-------|----------|----------|-------------|
| **Starter** | R$ 299/mês | 5 | 10 | 500 |
| **Professional** | R$ 599/mês | 15 | 30 | Ilimitado |
| **Enterprise** | R$ 1.499/mês | Ilimitado | Ilimitado | Ilimitado |

### Como fazer upgrade do plano?
1. Menu → **Configurações** → **Meu Plano**
2. Clique em **Fazer Upgrade**
3. Selecione o novo plano
4. Confirme o pagamento
5. Upgrade é imediato!

### Posso cancelar a qualquer momento?
Sim! Não há fidelidade. Cancele quando quiser:
1. Menu → **Configurações** → **Meu Plano**
2. Clique em **Cancelar Assinatura**
3. Confirme

Você terá acesso até o fim do período pago.

### Quais formas de pagamento são aceitas?
- 💳 Cartão de crédito (Visa, Master, Elo, Amex)
- 🏦 Boleto bancário
- 📱 PIX

Pagamento processado via Mercado Pago (seguro e confiável).

### Há desconto para pagamento anual?
Sim! 20% de desconto no pagamento anual:
- Starter: R$ 2.870/ano (R$ 239/mês)
- Professional: R$ 5.750/ano (R$ 479/mês)
- Enterprise: R$ 14.390/ano (R$ 1.199/mês)

---

## 📞 Ainda tem dúvidas?

### Suporte
- 📧 **Email**: suporte@logiflow.com.br
- 💬 **WhatsApp**: (11) 99999-9999
- 🌐 **Base de Conhecimento**: docs.logiflow.com.br
- ⏰ **Horário**: Segunda a Sexta, 8h às 18h

### Treinamento
Oferecemos treinamento gratuito para novos clientes:
- 🎥 Vídeos tutoriais
- 📚 Documentação completa
- 👨‍🏫 Sessão de onboarding (1h)
- 💡 Suporte dedicado nos primeiros 30 dias

---

**Última atualização**: Dezembro 2024 | **Versão**: 1.0
