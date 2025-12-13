# Template de Importação - Veículos

## Instruções

1. Baixe o arquivo `template_veiculos.xlsx`
2. Preencha os dados seguindo as instruções abaixo
3. Não altere o nome das colunas (linha 1)
4. Salve o arquivo em formato Excel (.xlsx)

## Colunas do Template

| Coluna | Obrigatório | Descrição | Exemplo |
|--------|-------------|-----------|---------|
| placa | ✅ Sim | Placa do veículo | ABC1D23 |
| tipo | ✅ Sim | Tipo do veículo | truck |
| renavam | Não | Código RENAVAM | 12345678901 |
| chassi | Não | Número do chassi | 9BWZZZ377VT004251 |
| marca | Não | Marca | Volvo |
| modelo | Não | Modelo | FH 540 |
| ano_fabricacao | Não | Ano de fabricação | 2022 |
| ano_modelo | Não | Ano do modelo | 2023 |
| cor | Não | Cor | Branco |
| capacidade_kg | Não | Capacidade em kg | 30000 |
| capacidade_m3 | Não | Capacidade em m³ | 90 |
| propriedade | Não | Tipo de propriedade | proprio |
| proprietario_nome | Não | Nome do proprietário | João Silva |
| km_atual | Não | Quilometragem atual | 150000 |
| observacoes | Não | Observações | Rastreador instalado |

## Tipos de Veículo Aceitos

| Valor | Descrição |
|-------|-----------|
| `moto` | Motocicleta |
| `fiorino` | Fiorino/Kangoo |
| `van` | Van |
| `vuc` | VUC (3/4) |
| `toco` | Caminhão Toco |
| `truck` | Caminhão Truck |
| `carreta` | Carreta |
| `bitrem` | Bitrem |
| `rodotrem` | Rodotrem |

## Tipos de Propriedade Aceitos

- `proprio` (padrão)
- `terceiro`
- `agregado`
- `alugado`

## Formato da Placa

Aceita os formatos:
- Mercosul: `ABC1D23`
- Antigo: `ABC-1234`

A placa será padronizada automaticamente (sem hífen, maiúsculas).

## Comando de Importação

```bash
python manage.py importar_dados template_veiculos.xlsx veiculos --tenant=meu-tenant
```
