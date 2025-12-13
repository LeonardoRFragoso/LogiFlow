# Template de Importação - Clientes

## Instruções

1. Baixe o arquivo `template_clientes.xlsx`
2. Preencha os dados seguindo as instruções abaixo
3. Não altere o nome das colunas (linha 1)
4. Salve o arquivo em formato Excel (.xlsx)
5. Use o comando de importação ou a interface web

## Colunas do Template

| Coluna | Obrigatório | Descrição | Exemplo |
|--------|-------------|-----------|---------|
| razao_social | ✅ Sim | Razão social da empresa | Transportes ABC Ltda |
| nome_fantasia | Não | Nome fantasia | ABC Transportes |
| cnpj | ✅ Sim | CNPJ (com ou sem formatação) | 12.345.678/0001-90 |
| inscricao_estadual | Não | Inscrição estadual | 123456789 |
| contato_nome | Não | Nome do contato principal | João Silva |
| email | Não | E-mail de contato | contato@abc.com.br |
| telefone | Não | Telefone fixo | (11) 3333-4444 |
| celular | Não | Celular/WhatsApp | (11) 99999-8888 |
| cep | Não | CEP do endereço | 01310-100 |
| logradouro | Não | Rua/Avenida | Av. Paulista |
| numero | Não | Número | 1000 |
| complemento | Não | Complemento | Sala 101 |
| bairro | Não | Bairro | Bela Vista |
| cidade | Não | Cidade | São Paulo |
| uf | Não | Estado (2 letras) | SP |
| condicao_pagamento | Não | Condição de pagamento | 30 dias |
| observacoes | Não | Observações gerais | Cliente desde 2020 |

## Condições de Pagamento Aceitas

- `a vista` ou `à vista`
- `7 dias`
- `14 dias`
- `21 dias`
- `28 dias`
- `30 dias` (padrão)
- `45 dias`
- `60 dias`
- `faturado`

## Comando de Importação

```bash
python manage.py importar_dados template_clientes.xlsx clientes --tenant=meu-tenant

# Para simular sem salvar:
python manage.py importar_dados template_clientes.xlsx clientes --tenant=meu-tenant --dry-run
```
