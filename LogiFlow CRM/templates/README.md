# 📥 Templates de Migração de Dados - LogiFlow CRM

## 📋 Visão Geral

Esta pasta contém templates Excel para facilitar a migração de dados de sistemas antigos para o LogiFlow CRM.

---

## 📁 Templates Disponíveis

### 1. `template_clientes.xlsx`
**Importa**: Cadastro de clientes/empresas

**Campos obrigatórios**:
- Nome/Razão Social
- CNPJ/CPF
- Email
- Telefone

**Campos opcionais**:
- Endereço completo
- Condição de pagamento
- Observações

---

### 2. `template_motoristas.xlsx`
**Importa**: Cadastro de motoristas

**Campos obrigatórios**:
- Nome completo
- CPF
- CNH (número)
- Categoria CNH

**Campos opcionais**:
- Data de nascimento
- Telefone
- Endereço
- Data de vencimento CNH
- Status (Ativo/Inativo)

---

### 3. `template_veiculos.xlsx`
**Importa**: Cadastro de veículos da frota

**Campos obrigatórios**:
- Placa
- Tipo (Caminhão/Van/Carreta/etc)
- Marca
- Modelo

**Campos opcionais**:
- Ano fabricação
- Ano modelo
- Renavam
- Chassi
- Capacidade (kg)
- Status
- Data última manutenção

---

### 4. `template_cotacoes_historico.xlsx`
**Importa**: Histórico de cotações/pedidos

**Campos obrigatórios**:
- Cliente (Nome ou CNPJ)
- Origem (CEP ou Cidade/UF)
- Destino (CEP ou Cidade/UF)
- Valor
- Data

**Campos opcionais**:
- Status
- Peso (kg)
- Volumes
- Tipo de carga
- Observações

---

## 🔄 Processo de Migração

### Passo 1: Preparar os Dados
1. Baixe o template correspondente
2. Preencha com seus dados
3. **NÃO altere os nomes das colunas**
4. **NÃO adicione ou remova colunas**
5. Salve como `.xlsx` (Excel)

### Passo 2: Validar
```bash
cd backend
python scripts/validar_importacao.py --arquivo ../templates/meus_clientes.xlsx --tipo clientes
```

O script irá:
- ✅ Verificar campos obrigatórios
- ✅ Validar formatos (CPF, CNPJ, CEP, etc)
- ✅ Identificar duplicatas
- ✅ Gerar relatório de erros

### Passo 3: Importar
```bash
python scripts/importar_dados.py --arquivo ../templates/meus_clientes.xlsx --tipo clientes
```

Opções:
- `--dry-run`: Simula a importação sem salvar
- `--force`: Ignora avisos e importa mesmo assim
- `--update`: Atualiza registros existentes

---

## ⚠️ Regras Importantes

### Formatação de Dados

**CPF**: `123.456.789-00` ou `12345678900`
**CNPJ**: `12.345.678/0001-00` ou `12345678000100`
**Telefone**: `(11) 98888-8888` ou `11988888888`
**CEP**: `12345-678` ou `12345678`
**Data**: `DD/MM/AAAA` ou `AAAA-MM-DD`

### Campos Especiais

**Status**: `Ativo`, `Inativo`, `Bloqueado`
**Tipo de Veículo**: `Caminhão`, `Van`, `Carreta`, `Bitrem`, `Truck`
**Categoria CNH**: `A`, `B`, `C`, `D`, `E`, `AB`, `AC`, `AD`, `AE`
**Condição Pagamento**: `À vista`, `30 dias`, `60 dias`, `90 dias`

---

## 📊 Limites de Importação

| Template | Registros por vez | Tempo estimado |
|----------|-------------------|----------------|
| Clientes | 1.000 | ~2 minutos |
| Motoristas | 500 | ~1 minuto |
| Veículos | 500 | ~1 minuto |
| Cotações | 5.000 | ~10 minutos |

Para volumes maiores, divida em múltiplos arquivos.

---

## 🐛 Problemas Comuns

### "Campo obrigatório vazio"
**Solução**: Preencha todos os campos marcados como obrigatórios

### "CPF/CNPJ inválido"
**Solução**: Verifique se o número está correto e com dígitos verificadores válidos

### "Registro duplicado"
**Solução**: Use `--update` para atualizar ou remova duplicatas manualmente

### "Formato de data inválido"
**Solução**: Use formato DD/MM/AAAA (ex: 15/12/2024)

---

## 📞 Suporte

Dúvidas sobre migração:
- 📧 Email: suporte@logiflow.com.br
- 💬 WhatsApp: (11) 99999-9999
- 📖 Documentação: docs.logiflow.com.br/migracao

---

## ✅ Checklist de Migração

- [ ] Baixei os templates corretos
- [ ] Preenchi todos os campos obrigatórios
- [ ] Validei os dados com o script
- [ ] Corrigi os erros apontados
- [ ] Fiz backup dos dados originais
- [ ] Testei com `--dry-run`
- [ ] Executei a importação
- [ ] Conferi os dados no sistema
- [ ] Arquivei os templates usados

---

**Última atualização**: Dezembro 2024
