# 🧪 LogiFlow CRM - Test Suite

## 📋 Visão Geral

Suite completa de testes automatizados para o LogiFlow CRM, cobrindo:
- ✅ Autenticação e JWT
- ✅ Multi-Tenancy e Isolamento
- ✅ RBAC e Auditoria
- ✅ Billing e Planos
- ✅ Integrações Externas (GPS, Frete, ERP)

---

## 🚀 Executar Testes

### Instalar Dependências

```bash
pip install -r requirements-test.txt
```

### Executar Todos os Testes

```bash
pytest
```

### Executar com Cobertura

```bash
pytest --cov=. --cov-report=html
```

Relatório em: `htmlcov/index.html`

### Executar Testes Específicos

```bash
# Por arquivo
pytest tests/test_auth.py

# Por classe
pytest tests/test_auth.py::TestAuth

# Por função
pytest tests/test_auth.py::TestAuth::test_login_sucesso

# Por marker
pytest -m auth
pytest -m integration
pytest -m "not slow"
```

---

## 🏷️ Markers Disponíveis

- `@pytest.mark.unit` - Testes unitários
- `@pytest.mark.integration` - Testes de integração
- `@pytest.mark.slow` - Testes lentos (podem ser pulados)
- `@pytest.mark.auth` - Testes de autenticação
- `@pytest.mark.multitenancy` - Testes de multi-tenancy
- `@pytest.mark.billing` - Testes de billing
- `@pytest.mark.external` - Testes que chamam APIs externas (devem usar mocks)

---

## 📂 Estrutura de Testes

```
tests/
├── __init__.py                 # Módulo de testes
├── conftest.py                 # Fixtures compartilhadas
├── test_auth.py                # Testes de autenticação
├── test_multitenancy.py        # Testes de multi-tenancy
├── test_credentials.py         # Testes de credenciais
├── test_billing.py             # Testes de billing
└── test_integrations.py        # Testes de integrações
```

---

## 🛠️ Fixtures Disponíveis

### `test_db`
Banco de dados SQLite em memória para testes.

```python
def test_exemplo(test_db):
    # Usar test_db para queries
    result = test_db.execute("SELECT * FROM users")
```

### `client`
Cliente de teste FastAPI.

```python
def test_endpoint(client):
    response = client.get("/api/v1/entregas")
    assert response.status_code == 200
```

### `auth_headers`
Headers com autenticação de usuário comum.

```python
def test_protegido(client, auth_headers):
    response = client.get("/api/v1/entregas", headers=auth_headers)
    assert response.status_code == 200
```

### `admin_headers`
Headers com autenticação de admin.

```python
def test_admin_only(client, admin_headers):
    response = client.delete("/api/v1/users/123", headers=admin_headers)
    assert response.status_code == 204
```

---

## 📊 Cobertura de Testes

### Meta de Cobertura

- **Mínimo**: 70%
- **Ideal**: 85%+

### Áreas Críticas (100% de cobertura)

1. **Autenticação**
   - Login/Logout
   - Refresh token
   - Validação de JWT

2. **Multi-Tenancy**
   - Isolamento de dados
   - Resolução de tenant
   - Middleware

3. **RBAC**
   - Verificação de permissões
   - Auditoria de ações sensíveis

4. **Billing**
   - Verificação de limites
   - Bloqueio de features

---

## 🔧 Configuração

### pytest.ini

Configurações globais do pytest:
- Paths de teste
- Markers
- Opções de cobertura
- Formato de logs

### conftest.py

Fixtures compartilhadas:
- Banco de dados de teste
- Cliente HTTP
- Headers de autenticação
- Mocks de integrações

---

## 📝 Boas Práticas

### 1. Nomenclatura

```python
# ✅ BOM
def test_login_com_credenciais_validas():
    pass

# ❌ RUIM
def test_1():
    pass
```

### 2. Arrange-Act-Assert

```python
def test_criar_cliente():
    # Arrange
    dados = {"nome": "Cliente Teste"}
    
    # Act
    response = client.post("/clientes", json=dados)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["nome"] == "Cliente Teste"
```

### 3. Isolamento

```python
# ✅ BOM - Cada teste é independente
def test_a(test_db):
    test_db.add(User(email="a@test.com"))
    test_db.commit()

def test_b(test_db):
    test_db.add(User(email="b@test.com"))
    test_db.commit()

# ❌ RUIM - Testes dependem um do outro
estado_global = {}

def test_a():
    estado_global["user"] = create_user()

def test_b():
    user = estado_global["user"]  # Falha se test_a não rodar
```

### 4. Mocks para Integrações

```python
# ✅ BOM - Mock de API externa
@pytest.mark.external
def test_gps_sascar(mocker):
    mock_response = {"posicao": {"lat": -23.5, "lng": -46.6}}
    mocker.patch("integrations.gps.sascar.get_posicao", return_value=mock_response)
    
    response = client.get("/gps/posicao/ABC1234")
    assert response.status_code == 200

# ❌ RUIM - Chamada real (lento, instável, custa dinheiro)
def test_gps_sascar():
    response = client.get("/gps/posicao/ABC1234")  # Chama API real
```

---

## 🐛 Debug de Testes

### Ver output detalhado

```bash
pytest -vv -s
```

### Parar no primeiro erro

```bash
pytest -x
```

### Executar apenas testes que falharam

```bash
pytest --lf
```

### Debug com pdb

```python
def test_exemplo():
    import pdb; pdb.set_trace()
    # Código de teste
```

---

## 📈 CI/CD

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements-test.txt
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)

---

## ✅ Checklist Antes de Commit

- [ ] Todos os testes passam (`pytest`)
- [ ] Cobertura >= 70% (`pytest --cov`)
- [ ] Sem warnings (`pytest --strict-warnings`)
- [ ] Linting OK (`flake8 .`)
- [ ] Formatação OK (`black . --check`)
- [ ] Imports ordenados (`isort . --check`)
- [ ] Segurança OK (`bandit -r .`)

