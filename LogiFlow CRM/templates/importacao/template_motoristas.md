# Template de Importação - Motoristas

## Instruções

1. Baixe o arquivo `template_motoristas.xlsx`
2. Preencha os dados seguindo as instruções abaixo
3. Não altere o nome das colunas (linha 1)
4. Salve o arquivo em formato Excel (.xlsx)

## Colunas do Template

| Coluna | Obrigatório | Descrição | Exemplo |
|--------|-------------|-----------|---------|
| nome | ✅ Sim | Nome completo | José da Silva |
| cpf | ✅ Sim | CPF (com ou sem formatação) | 123.456.789-00 |
| rg | Não | RG | 12.345.678-9 |
| cnh_numero | ✅ Sim | Número da CNH | 12345678900 |
| cnh_categoria | ✅ Sim | Categoria da CNH | E |
| cnh_validade | ✅ Sim | Data de validade | 31/12/2025 |
| telefone | Não | Telefone fixo | (11) 3333-4444 |
| celular | Não | Celular/WhatsApp | (11) 99999-8888 |
| email | Não | E-mail | jose@email.com |
| cep | Não | CEP | 01310-100 |
| endereco | Não | Endereço completo | Rua das Flores, 123 |
| cidade | Não | Cidade | São Paulo |
| uf | Não | Estado (2 letras) | SP |
| status | Não | Status do motorista | ativo |
| observacoes | Não | Observações | Experiência com carreta |

## Categorias de CNH Aceitas

- `A` - Motocicleta
- `B` - Carro
- `C` - Caminhão
- `D` - Ônibus
- `E` - Carreta
- `AB`, `AC`, `AD`, `AE`

## Status Aceitos

- `ativo` (padrão)
- `inativo`
- `ferias`
- `afastado`
- `desligado`

## Formato de Data

Aceita os formatos:
- `DD/MM/AAAA` (31/12/2025)
- `AAAA-MM-DD` (2025-12-31)
- `DD-MM-AAAA` (31-12-2025)

## Comando de Importação

```bash
python manage.py importar_dados template_motoristas.xlsx motoristas --tenant=meu-tenant
```
