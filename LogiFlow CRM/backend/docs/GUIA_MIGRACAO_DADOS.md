# Guia de Migração de Dados - LogiFlow CRM

## Visão Geral

Este guia explica como migrar dados de sistemas antigos (planilhas, outros softwares) para o LogiFlow CRM usando os templates CSV e o script de importação automatizado.

## 📋 Processo de Migração (5 Passos)

```
1. COLETA (Dia 1)
   └── Cliente envia planilhas/exports
   └── Download dos templates LogiFlow

2. VALIDAÇÃO (Dia 1-2)
   └── Script valida dados automaticamente
   └── Relatório de inconsistências gerado
   └── Cliente corrige ou aprova "como está"

3. MAPEAMENTO (Dia 2)
   └── Campos origem → campos LogiFlow
   └── Regras de transformação aplicadas

4. IMPORTAÇÃO (Dia 2)
   └── Dry-run (simulação) primeiro
   └── Importação real após aprovação

5. VALIDAÇÃO FINAL (Dia 3)
   └── Conferência no sistema
   └── Ajustes se necessário
```

---

## 📁 Templates Disponíveis

### 1. Template de Clientes
**Arquivo:** `backend/templates/template_clientes.csv`

**Campos:**
| Campo | Obrigatório | Formato | Exemplo |
|-------|-------------|---------|---------|
| nome | ✅ Sim | Texto | "Transportadora ABC Ltda" |
| nome_fantasia | Não | Texto | "ABC Transportes" |
| cnpj | ✅ Sim* | 14 dígitos | "12345678000190" |
| cpf | ✅ Sim* | 11 dígitos | "12345678901" |
| ie | Não | Texto | "123456789" |
| tipo_pessoa | Não | J ou F | "J" |
| telefone | Não | 10-11 dígitos | "1133334444" |
| celular | Não | 10-11 dígitos | "11999998888" |
| email | Não | Email válido | "contato@abc.com.br" |
| endereco | Não | Texto | "Rua das Flores" |
| numero | Não | Texto | "100" |
| complemento | Não | Texto | "Sala 5" |
| bairro | Não | Texto | "Centro" |
| cidade | Não | Texto | "São Paulo" |
| uf | Não | 2 letras | "SP" |
| cep | Não | 8 dígitos | "01310100" |
| contato_principal | Não | Texto | "João Silva" |
| observacoes | Não | Texto | "Cliente desde 2020" |

*CPF ou CNPJ é obrigatório (um dos dois)

---

### 2. Template de Motoristas
**Arquivo:** `backend/templates/template_motoristas.csv`

**Campos:**
| Campo | Obrigatório | Formato | Exemplo |
|-------|-------------|---------|---------|
| nome | ✅ Sim | Texto | "José da Silva" |
| cpf | ✅ Sim | 11 dígitos | "11122233344" |
| rg | Não | Texto | "123456789" |
| cnh | ✅ Sim | 11 dígitos | "12345678901" |
| categoria_cnh | ✅ Sim | A, B, C, D, E | "E" |
| vencimento_cnh | Não | YYYY-MM-DD | "2025-12-31" |
| data_nascimento | Não | YYYY-MM-DD | "1985-05-15" |
| telefone | Não | 10-11 dígitos | "1133334444" |
| celular | Não | 10-11 dígitos | "11999998888" |
| email | Não | Email válido | "jose@email.com" |
| endereco | Não | Texto | "Rua A" |
| numero | Não | Texto | "10" |
| complemento | Não | Texto | "Apto 5" |
| bairro | Não | Texto | "Jardim" |
| cidade | Não | Texto | "São Paulo" |
| uf | Não | 2 letras | "SP" |
| cep | Não | 8 dígitos | "01000100" |
| status | Não | ativo/inativo | "ativo" |
| observacoes | Não | Texto | "Motorista experiente" |

---

### 3. Template de Veículos
**Arquivo:** `backend/templates/template_veiculos.csv`

**Campos:**
| Campo | Obrigatório | Formato | Exemplo |
|-------|-------------|---------|---------|
| placa | ✅ Sim | ABC1234 ou ABC1D23 | "ABC1234" |
| renavam | Não | 11 dígitos | "12345678901" |
| tipo | ✅ Sim | Texto | "Caminhão" |
| marca | Não | Texto | "Mercedes-Benz" |
| modelo | Não | Texto | "Atego 1719" |
| ano_fabricacao | Não | YYYY | "2020" |
| ano_modelo | Não | YYYY | "2021" |
| cor | Não | Texto | "Branco" |
| chassi | Não | 17 caracteres | "9BM123456789012345" |
| capacidade_kg | Não | Número | "7000" |
| capacidade_m3 | Não | Número | "30" |
| status | Não | ativo/inativo/manutencao | "ativo" |
| proprietario | Não | Texto | "Empresa" |
| ultima_manutencao | Não | YYYY-MM-DD | "2024-11-15" |
| proxima_manutencao | Não | YYYY-MM-DD | "2025-02-15" |
| observacoes | Não | Texto | "Veículo em ótimo estado" |

---

### 4. Template de Cotações (Histórico)
**Arquivo:** `backend/templates/template_cotacoes.csv`

**Campos:**
| Campo | Obrigatório | Formato | Exemplo |
|-------|-------------|---------|---------|
| numero | ✅ Sim | Texto | "COT-2024-00001" |
| cliente_nome | ✅ Sim | Texto | "Transportadora ABC" |
| cliente_cnpj | Não | 14 dígitos | "12345678000190" |
| data_cotacao | Não | YYYY-MM-DD | "2024-01-15" |
| origem_cep | ✅ Sim | 8 dígitos | "01310100" |
| origem_cidade | Não | Texto | "São Paulo" |
| origem_uf | Não | 2 letras | "SP" |
| destino_cep | ✅ Sim | 8 dígitos | "04101300" |
| destino_cidade | Não | Texto | "São Paulo" |
| destino_uf | Não | 2 letras | "SP" |
| tipo_carga | Não | fracionada/lotacao/container | "fracionada" |
| peso_kg | ✅ Sim | Número | "500" |
| volume_m3 | Não | Número | "2" |
| valor_mercadoria | Não | Número | "5000" |
| tipo_frete | Não | CIF/FOB | "CIF" |
| valor_frete | Não | Número | "450.00" |
| valor_pedagio | Não | Número | "80.00" |
| valor_seguro | Não | Número | "50.00" |
| valor_outros | Não | Número | "20.00" |
| desconto | Não | Número | "0" |
| valor_total | Não | Número | "600.00" |
| prazo_dias | Não | Número | "3" |
| status | Não | rascunho/enviada/aprovada/rejeitada/convertida | "aprovada" |
| observacoes | Não | Texto | "Entrega urgente" |

---

## 🚀 Como Usar o Script de Importação

### Instalação

```bash
cd backend
pip install -r requirements.txt
```

### Uso Básico

```bash
# Importar clientes
python scripts/importar_dados.py --tipo clientes --arquivo templates/template_clientes.csv

# Importar motoristas
python scripts/importar_dados.py --tipo motoristas --arquivo templates/template_motoristas.csv

# Importar veículos
python scripts/importar_dados.py --tipo veiculos --arquivo templates/template_veiculos.csv

# Importar cotações
python scripts/importar_dados.py --tipo cotacoes --arquivo templates/template_cotacoes.csv
```

### Modo Dry-Run (Simulação)

**SEMPRE execute em modo dry-run primeiro!**

```bash
# Simular importação (não grava dados)
python scripts/importar_dados.py --tipo clientes --arquivo meus_clientes.csv --dry-run
```

O modo dry-run:
- ✅ Valida todos os dados
- ✅ Gera relatório de erros
- ✅ Mostra o que seria importado
- ❌ NÃO grava nada no banco

---

## 📊 Relatório de Importação

Após cada importação, um relatório JSON é gerado:

```json
{
  "tipo": "clientes",
  "timestamp": "20241214_143000",
  "dry_run": false,
  "total": 10,
  "sucessos": 8,
  "erros": [
    "Linha 3 (Cliente XYZ): CNPJ inválido: 123",
    "Linha 7 (Cliente ABC): Email inválido: abc@"
  ],
  "avisos": [
    "Linha 5: Telefone pode estar inválido: 123"
  ]
}
```

---

## ✅ Validações Automáticas

### Clientes
- ✅ CPF ou CNPJ obrigatório e válido
- ✅ CEP com 8 dígitos
- ✅ Email no formato correto
- ⚠️ Telefone com 10-11 dígitos (aviso)

### Motoristas
- ✅ CPF obrigatório e válido
- ✅ CNH obrigatória
- ✅ Categoria CNH obrigatória
- ⚠️ CNH vencida (aviso)
- ⚠️ Telefone inválido (aviso)

### Veículos
- ✅ Placa obrigatória e válida (formato antigo ou Mercosul)
- ✅ Tipo obrigatório
- ✅ Capacidade maior que zero
- ⚠️ Marca não informada (aviso)
- ⚠️ Modelo não informado (aviso)

### Cotações
- ✅ Número obrigatório
- ✅ Cliente obrigatório
- ✅ CEPs origem e destino válidos
- ✅ Peso maior que zero
- ✅ Valor total não negativo

---

## 🔧 Preparando Seus Dados

### 1. Exportar do Sistema Antigo

**Excel/Planilhas:**
- Salvar como CSV (UTF-8)
- Separador: vírgula (,)
- Codificação: UTF-8

**Outros Sistemas:**
- Exportar para CSV ou Excel
- Converter para CSV se necessário

### 2. Limpar os Dados

**Remover:**
- Linhas em branco
- Caracteres especiais desnecessários
- Espaços extras

**Padronizar:**
- CPF/CNPJ: apenas números
- CEP: apenas números
- Telefone: apenas números
- Datas: formato YYYY-MM-DD

### 3. Mapear Campos

Crie uma tabela de mapeamento:

| Campo Sistema Antigo | Campo LogiFlow | Transformação |
|---------------------|----------------|---------------|
| razao_social | nome | Direto |
| cnpj_empresa | cnpj | Remover pontuação |
| fone | telefone | Remover pontuação |
| email_contato | email | Direto |

---

## 📝 Exemplo Prático

### Passo 1: Download do Template

```bash
# Baixar template de clientes
cp backend/templates/template_clientes.csv meus_clientes.csv
```

### Passo 2: Preencher com Seus Dados

Abra `meus_clientes.csv` no Excel e preencha:

```csv
nome,cnpj,telefone,email,cidade,uf
"Empresa A","12345678000190","1133334444","a@empresa.com","São Paulo","SP"
"Empresa B","98765432000111","1144445555","b@empresa.com","Campinas","SP"
```

### Passo 3: Validar (Dry-Run)

```bash
python scripts/importar_dados.py --tipo clientes --arquivo meus_clientes.csv --dry-run
```

**Saída:**
```
=== Importando Clientes ===

✓ Cliente: Empresa A
✓ Cliente: Empresa B

============================================================
RELATÓRIO DE IMPORTAÇÃO - CLIENTES
============================================================

⚠ MODO DRY-RUN (Simulação) - Nenhum dado foi importado

Total de registros processados: 2
✓ Sucessos: 2
✗ Erros: 0
⚠ Avisos: 0

✓ Importação concluída com sucesso!
============================================================
```

### Passo 4: Importar de Verdade

```bash
python scripts/importar_dados.py --tipo clientes --arquivo meus_clientes.csv
```

---

## ⚠️ Problemas Comuns

### Erro: "CNPJ inválido"
**Causa:** CNPJ com pontuação ou incompleto  
**Solução:** Usar apenas números, 14 dígitos

### Erro: "CEP inválido"
**Causa:** CEP com hífen ou incompleto  
**Solução:** Usar apenas números, 8 dígitos

### Erro: "Email inválido"
**Causa:** Email sem @ ou domínio  
**Solução:** Verificar formato: usuario@dominio.com

### Erro: "Placa inválida"
**Causa:** Placa fora do padrão  
**Solução:** Usar formato ABC1234 ou ABC1D23

### Aviso: "CNH vencida"
**Causa:** Data de vencimento no passado  
**Solução:** Atualizar CNH ou importar mesmo assim

---

## 📞 Suporte

Dúvidas sobre migração:
- Email: suporte@logiflow.com.br
- Documentação: https://docs.logiflow.com.br/migracao
- WhatsApp: (11) 99999-9999

---

## 🎯 Checklist de Migração

- [ ] Baixar templates
- [ ] Exportar dados do sistema antigo
- [ ] Limpar e padronizar dados
- [ ] Preencher templates
- [ ] Executar dry-run
- [ ] Corrigir erros
- [ ] Importar dados reais
- [ ] Validar no sistema
- [ ] Conferir relatórios
- [ ] Treinar usuários

---

**Tempo estimado:** 2-3 dias  
**Dificuldade:** Média  
**Suporte:** Incluído no onboarding
