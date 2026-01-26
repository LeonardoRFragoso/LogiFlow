# LogiFlow CRM - Code Standards

> Padrões de código e convenções do projeto

## Python (Backend)

### Estilo de Código

- **Formatter:** Black (linha máxima: 88 caracteres)
- **Linter:** Ruff
- **Type Checker:** mypy (opcional)

### Convenções de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Variáveis | snake_case | `cliente_id` |
| Funções | snake_case | `criar_cliente()` |
| Classes | PascalCase | `ClienteRepository` |
| Constantes | UPPER_SNAKE | `MAX_RETRIES` |
| Arquivos | snake_case | `cliente_repository.py` |
| Módulos | snake_case | `use_cases` |

### Estrutura de Imports

```python
# 1. Standard library
import os
import sys
from datetime import datetime
from typing import List, Optional

# 2. Third-party
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

# 3. Local application
from domain.entities import Cliente
from infrastructure.repositories import ClienteRepository
```

### Docstrings

```python
def criar_cliente(dto: ClienteCreateDTO, tenant_id: str) -> ClienteResponseDTO:
    """
    Cria um novo cliente no sistema.
    
    Args:
        dto: Dados do cliente a ser criado
        tenant_id: ID do tenant atual
    
    Returns:
        ClienteResponseDTO: Cliente criado
    
    Raises:
        ValueError: Se CNPJ já existir
    """
    pass
```

### Type Hints

```python
# ✅ Correto
def get_cliente(id: str) -> Optional[Cliente]:
    pass

def listar_clientes(skip: int = 0, limit: int = 100) -> List[Cliente]:
    pass

# ❌ Incorreto
def get_cliente(id):
    pass
```

---

## Vue.js (Frontend)

### Estilo de Código

- **Linter:** ESLint + Vue plugin
- **Formatter:** Prettier (integrado)

### Convenções de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Componentes | PascalCase | `ClienteForm.vue` |
| Composables | camelCase com `use` | `useClientes.js` |
| Stores | camelCase | `clienteStore.js` |
| Services | camelCase | `apiService.js` |
| Eventos | kebab-case | `@cliente-criado` |
| Props | camelCase | `:clienteId` |

### Estrutura de Componente

```vue
<script setup>
// 1. Imports
import { ref, computed, onMounted } from 'vue'
import { useClienteStore } from '@/stores/cliente'

// 2. Props & Emits
const props = defineProps({
  clienteId: { type: String, required: true }
})

const emit = defineEmits(['cliente-atualizado'])

// 3. Composables & Stores
const store = useClienteStore()

// 4. Reactive State
const loading = ref(false)
const cliente = ref(null)

// 5. Computed
const nomeFormatado = computed(() => 
  cliente.value?.razao_social?.toUpperCase()
)

// 6. Methods
async function salvar() {
  loading.value = true
  try {
    await store.atualizar(cliente.value)
    emit('cliente-atualizado')
  } finally {
    loading.value = false
  }
}

// 7. Lifecycle
onMounted(() => {
  carregarCliente()
})
</script>

<template>
  <div class="cliente-form">
    <!-- Template content -->
  </div>
</template>

<style scoped>
.cliente-form {
  /* Styles */
}
</style>
```

---

## Testes

### Nomenclatura de Testes

```python
# Arquivo: test_cliente_use_cases.py

class TestCriarClienteUseCase:
    """Testes para o caso de uso CriarCliente."""
    
    def test_criar_cliente_com_dados_validos(self):
        """Deve criar cliente quando dados são válidos."""
        pass
    
    def test_criar_cliente_com_cnpj_duplicado_deve_falhar(self):
        """Deve lançar erro quando CNPJ já existe."""
        pass
    
    def test_criar_cliente_sem_razao_social_deve_falhar(self):
        """Deve lançar erro quando razão social está vazia."""
        pass
```

### Padrão AAA

```python
def test_aprovar_cotacao(self):
    # Arrange (Preparação)
    cotacao = CotacaoFactory.create(status=StatusCotacao.PENDENTE)
    mock_repo = Mock(spec=ICotacaoRepository)
    mock_repo.get_by_id.return_value = cotacao
    use_case = AprovarCotacaoUseCase(mock_repo)
    
    # Act (Ação)
    resultado = use_case.execute(cotacao.id)
    
    # Assert (Verificação)
    assert resultado.status == StatusCotacao.APROVADA
    mock_repo.update.assert_called_once()
```

---

## Git

### Commits (Conventional Commits)

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não altera código)
- `refactor`: Refatoração
- `test`: Adição/correção de testes
- `chore`: Tarefas de manutenção

**Exemplos:**
```
feat(clientes): adiciona endpoint de busca por CNPJ
fix(auth): corrige expiração de token JWT
docs(api): atualiza documentação de endpoints
refactor(cotacoes): extrai lógica para use case
test(billing): adiciona testes de integração
```

### Branches

- `main`: Produção
- `develop`: Desenvolvimento
- `feature/xxx`: Nova funcionalidade
- `fix/xxx`: Correção de bug
- `hotfix/xxx`: Correção urgente em produção

---

## Checklist de Code Review

### Python
- [ ] Type hints em todas as funções públicas
- [ ] Docstrings em classes e funções públicas
- [ ] Sem imports não utilizados
- [ ] Testes para nova funcionalidade
- [ ] Sem secrets hardcoded

### Vue.js
- [ ] Props tipadas com `defineProps`
- [ ] Eventos declarados com `defineEmits`
- [ ] Componentes extraídos quando > 200 linhas
- [ ] Sem console.log em produção
- [ ] Estilos com `scoped`

### Geral
- [ ] Commit messages seguem Conventional Commits
- [ ] Branch nomeada corretamente
- [ ] CI passou sem erros
- [ ] Documentação atualizada se necessário
