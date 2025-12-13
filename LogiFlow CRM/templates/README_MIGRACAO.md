# Templates de Migração de Dados - LogiFlow CRM

Este diretório contém templates Excel para migração de dados de sistemas legados para o LogiFlow CRM.

## 📋 Templates Disponíveis

### 1. template_clientes.csv
Migração de clientes (transportadoras)

**Campos obrigatórios:**
- `nome` - Nome da empresa
- `cnpj` - CNPJ (apenas números)
- `email` - E-mail principal

**Campos opcionais:**
- `telefone` - Telefone principal
- `endereco` - Endereço completo
- `cidade` - Cidade
- `uf` - Estado (sigla)
- `cep` - CEP
- `contato_nome` - Nome do contato principal
- `contato_telefone` - Telefone do contato
- `condicao_pagamento` - Ex: "30 dias", "À vista"
- `observacoes` - Observações gerais

### 2. template_motoristas.csv
Migração de motoristas

**Campos obrigatórios:**
- `nome` - Nome completo
- `cpf` - CPF (apenas números)
- `cnh` - Número da CNH
- `categoria_cnh` - A, B, C, D, E, AB, AC, AD, AE

**Campos opcionais:**
- `vencimento_cnh` - Data de vencimento (DD/MM/AAAA)
- `celular` - Telefone celular
- `email` - E-mail
- `status` - ativo, inativo, afastado
- `observacoes` - Observações

### 3. template_veiculos.csv
Migração de veículos

**Campos obrigatórios:**
- `placa` - Placa do veículo
- `tipo_veiculo` - caminhao_toco, caminhao_truck, carreta, bitrem, van, utilitario

**Campos opcionais:**
- `renavam` - Número do RENAVAM
- `marca` - Marca do veículo
- `modelo` - Modelo
- `ano_fabricacao` - Ano de fabricação
- `ano_modelo` - Ano do modelo
- `capacidade_kg` - Capacidade em kg
- `crlv_validade` - Validade do CRLV (DD/MM/AAAA)
- `status` - disponivel, em_uso, manutencao, inativo
- `observacoes` - Observações

### 4. template_cotacoes.csv
Migração de cotações históricas

**Campos obrigatórios:**
- `cliente_cnpj` - CNPJ do cliente
- `origem_cidade` - Cidade de origem
- `origem_uf` - UF de origem
- `destino_cidade` - Cidade de destino
- `destino_uf` - UF de destino
- `valor_proposta` - Valor da proposta

**Campos opcionais:**
- `data_cotacao` - Data da cotação (DD/MM/AAAA)
- `tipo_carga` - geral, refrigerada, perigosa, fragil
- `peso_kg` - Peso em kg
- `status` - aberta, aprovada, perdida, expirada
- `validade` - Data de validade (DD/MM/AAAA)
- `observacoes` - Observações

## 🔧 Como Usar

### Passo 1: Baixar o Template
Baixe o template CSV correspondente aos dados que deseja migrar.

### Passo 2: Preencher os Dados
- Abra o arquivo no Excel, LibreOffice ou Google Sheets
- Preencha uma linha por registro
- **NÃO remova a linha de cabeçalho**
- **NÃO altere os nomes das colunas**
- Deixe células vazias para campos opcionais que não possui

### Passo 3: Validar os Dados
Antes de importar, verifique:
- ✅ CPF/CNPJ estão apenas com números (sem pontos, traços)
- ✅ Datas no formato DD/MM/AAAA
- ✅ Valores numéricos sem símbolos (ex: 1500.50, não R$ 1.500,50)
- ✅ Campos obrigatórios preenchidos
- ✅ Valores de enumeração corretos (status, tipo, etc.)

### Passo 4: Salvar como CSV
- Salve o arquivo como **CSV (separado por vírgulas)**
- Codificação: **UTF-8**

### Passo 5: Importar
Execute o script de importação:

```bash
python scripts/importar_dados.py --tipo clientes --arquivo template_clientes.csv
```

Ou use a interface web:
- Acesse: http://localhost:8000/admin/importacao
- Selecione o tipo de dados
- Faça upload do arquivo CSV
- Revise os dados
- Confirme a importação

## ⚠️ Avisos Importantes

### Duplicatas
O sistema verifica duplicatas por:
- **Clientes**: CNPJ
- **Motoristas**: CPF
- **Veículos**: Placa
- **Cotações**: Não verifica (permite duplicatas)

Se encontrar duplicata, o sistema:
- **Modo padrão**: Pula o registro e registra no log
- **Modo atualização**: Atualiza o registro existente (use com cuidado!)

### Validações
O sistema valida:
- ✅ Formato de CPF/CNPJ
- ✅ Formato de datas
- ✅ Valores numéricos
- ✅ Campos obrigatórios
- ✅ Valores de enumeração
- ✅ Relacionamentos (ex: cliente existe para cotação)

### Logs
Todos os erros e avisos são registrados em:
```
logs/importacao_YYYYMMDD_HHMMSS.log
```

### Rollback
Se algo der errado:
```bash
python scripts/importar_dados.py --rollback --importacao-id <ID>
```

## 📊 Exemplo de Preenchimento

### Clientes
```csv
nome,cnpj,email,telefone,cidade,uf,condicao_pagamento
"Transportadora ABC Ltda",12345678000190,contato@abc.com.br,11987654321,"São Paulo",SP,"30 dias"
"Logística XYZ S/A",98765432000110,comercial@xyz.com.br,21987654321,"Rio de Janeiro",RJ,"À vista"
```

### Motoristas
```csv
nome,cpf,cnh,categoria_cnh,vencimento_cnh,celular,status
"João da Silva",12345678901,12345678901,D,31/12/2025,11987654321,ativo
"Maria Santos",98765432109,98765432109,E,15/06/2026,11976543210,ativo
```

### Veículos
```csv
placa,tipo_veiculo,marca,modelo,ano_fabricacao,capacidade_kg,status
ABC1234,caminhao_truck,Mercedes-Benz,Atego 1719,2020,8000,disponivel
XYZ5678,carreta,Volvo,FH 540,2019,30000,em_uso
```

## 🆘 Suporte

Se encontrar problemas:
1. Verifique o arquivo de log
2. Valide o formato do CSV
3. Teste com poucos registros primeiro
4. Entre em contato: suporte@logiflow.com.br

## 📝 Changelog

### v1.0.0 (2024-12-12)
- Templates iniciais criados
- Validações implementadas
- Documentação completa
