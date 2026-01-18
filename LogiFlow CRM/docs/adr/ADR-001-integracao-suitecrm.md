# ADR-001: Integração do SuiteCRM como Sistema Legado Externo

## Status
Aprovada

## Contexto
O LogiFlow CRM está sendo desenvolvido como um sistema moderno, baseado em Django (backend) e Vue.js (frontend), com foco em arquitetura limpa, escalabilidade e testabilidade.

O SuiteCRM permanece como um sistema legado já utilizado pela organização. No repositório do LogiFlow existe um diretório `suitecrm` contendo scripts, documentação e referências históricas relacionadas a integrações e fluxos entre os sistemas.

## Decisão
- O SuiteCRM será tratado exclusivamente como **sistema legado externo**, sem qualquer acoplamento direto ao core do LogiFlow CRM.
- Apenas os seguintes artefatos poderão ser reaproveitados, mediante avaliação:
  - Mapeamentos de entidades
  - Exemplos de payloads e fluxos de integração
  - Documentação técnica relevante
- Não será reaproveitado:
  - Código legado não testado ou sem manutenção
  - Dependências desatualizadas
  - Configurações sensíveis ou dados reais
- Toda integração será realizada exclusivamente via **APIs públicas e documentadas do SuiteCRM**, encapsulada em um **app de integrações dedicado** no backend do LogiFlow CRM.
- Os fluxos de integração deverão ser:
  - Desacoplados do core
  - Assíncronos quando possível
  - Testáveis, com mocks e fixtures
  - Observáveis (logs e tratamento de falhas)

## Consequências
- Redução significativa de riscos de dívida técnica e falhas de segurança.
- Arquitetura mais limpa e sustentável no longo prazo.
- Maior facilidade de manutenção e evolução do LogiFlow CRM.
- Capacidade de descontinuar o SuiteCRM no futuro com impacto mínimo.

## Alternativas Consideradas e Descartadas
- Incorporar código legado do SuiteCRM diretamente ao core do LogiFlow CRM.
- Realizar integrações via acesso direto ao banco de dados do SuiteCRM.
- Manter dependências ou bibliotecas do SuiteCRM dentro do projeto LogiFlow.

## Notas
Esta decisão estabelece um limite arquitetural claro entre o LogiFlow CRM e sistemas legados, devendo ser respeitada em todas as implementações futuras.
