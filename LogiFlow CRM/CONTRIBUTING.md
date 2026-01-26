# Contribuindo para o LogiFlow CRM

Obrigado por considerar contribuir com o LogiFlow CRM! Este documento fornece as diretrizes para contribuir com o projeto.

## 📋 Código de Conduta

Este projeto segue um código de conduta simples: seja respeitoso e construtivo em todas as interações.

## 🚀 Como Contribuir

### 1. Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/LeonardoRFragoso/LogiFlow.git
cd "LogiFlow CRM"

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r backend/requirements.txt

# Instale pre-commit hooks
pip install pre-commit
pre-commit install

# Configure o ambiente
cp .env.example .env
```

### 2. Workflow de Contribuição

1. **Fork** o repositório
2. **Clone** seu fork: `git clone https://github.com/SEU_USUARIO/LogiFlow.git`
3. **Crie uma branch**: `git checkout -b feature/minha-feature`
4. **Faça suas mudanças**
5. **Rode os testes**: `pytest tests/unit -v`
6. **Commit**: `git commit -m 'feat: adiciona minha feature'`
7. **Push**: `git push origin feature/minha-feature`
8. **Abra um Pull Request**

### 3. Branches

| Branch | Propósito |
|--------|-----------|
| `main` | Código de produção |
| `develop` | Desenvolvimento ativo |
| `feature/*` | Novas funcionalidades |
| `bugfix/*` | Correções de bugs |
| `hotfix/*` | Correções urgentes em produção |

## 📝 Padrões de Commit

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé opcional]
```

### Tipos

| Tipo | Descrição |
|------|-----------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação (sem mudança de lógica) |
| `refactor` | Refatoração de código |
| `perf` | Melhoria de performance |
| `test` | Adição ou correção de testes |
| `chore` | Tarefas de manutenção |
| `ci` | Mudanças em CI/CD |

### Exemplos

```bash
feat(cotacoes): adiciona cálculo de frete por peso
fix(auth): corrige refresh token expirado
docs(api): atualiza documentação de endpoints
test(pedidos): adiciona testes para criação de pedido
```

## 🧪 Testes

### Executando Testes

```bash
# Todos os testes unitários
pytest tests/unit -v

# Com cobertura
pytest tests/unit --cov=. --cov-report=html

# Testes específicos
pytest tests/unit/test_entities.py -v

# Testes de integração
pytest tests/integration -v
```

### Escrevendo Testes

- Siga o padrão **AAA** (Arrange, Act, Assert)
- Use nomes descritivos: `test_create_pedido_with_valid_data_returns_success`
- Um assert por teste quando possível
- Mock de dependências externas

```python
def test_create_cotacao_with_valid_data():
    # Arrange
    data = {"origem": "SP", "destino": "RJ", "peso": 100}
    
    # Act
    result = cotacao_service.create(data)
    
    # Assert
    assert result.status == "created"
```

## 🎨 Padrões de Código

### Python (Backend)

- **Linter**: Ruff
- **Formatter**: Ruff format
- **Type hints**: Obrigatório para funções públicas
- **Docstrings**: Google style

```python
def calculate_freight(
    origin: str,
    destination: str,
    weight: float
) -> FreightResult:
    """
    Calcula o frete entre origem e destino.
    
    Args:
        origin: Cidade de origem
        destination: Cidade de destino  
        weight: Peso em kg
        
    Returns:
        FreightResult com valor e prazo
        
    Raises:
        InvalidRouteError: Se a rota não for válida
    """
    ...
```

### Vue.js (Frontend)

- **Linter**: ESLint
- **Style**: Composition API
- **Componentes**: PascalCase

## 📁 Estrutura do Projeto

```
LogiFlow CRM/
├── backend/
│   ├── domain/           # Entidades e regras de negócio
│   ├── application/      # Use cases e DTOs
│   ├── infrastructure/   # Banco, cache, APIs externas
│   ├── presentation/     # Routers da API (Clean Arch)
│   ├── routers/          # Routers legados
│   ├── services/         # Serviços de negócio
│   └── tests/            # Testes
├── frontend/
│   └── src/
│       ├── components/   # Componentes Vue
│       ├── views/        # Páginas
│       └── stores/       # Pinia stores
└── docs/                 # Documentação
```

## 🔍 Code Review

### Checklist para PRs

- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Não há secrets ou dados sensíveis
- [ ] CI passou com sucesso
- [ ] Commits seguem conventional commits

### O que revisamos

1. **Funcionalidade**: O código faz o que deveria?
2. **Testes**: Cobertura adequada?
3. **Performance**: Há gargalos óbvios?
4. **Segurança**: Há vulnerabilidades?
5. **Legibilidade**: O código é claro?

## 🐛 Reportando Bugs

Use o template de issue para bugs:

```markdown
## Descrição
[Descreva o bug]

## Passos para Reproduzir
1. Vá para '...'
2. Clique em '...'
3. Veja o erro

## Comportamento Esperado
[O que deveria acontecer]

## Screenshots
[Se aplicável]

## Ambiente
- OS: [ex: Windows 11]
- Browser: [ex: Chrome 120]
- Versão: [ex: 1.0.0]
```

## 💡 Sugerindo Features

1. Verifique se já não existe uma issue similar
2. Use o template de feature request
3. Explique o problema que a feature resolve
4. Descreva a solução proposta

## 📞 Contato

- **Email**: suporte@logiflow.com.br
- **Issues**: [GitHub Issues](https://github.com/LeonardoRFragoso/LogiFlow/issues)

---

Obrigado por contribuir! 🚀
