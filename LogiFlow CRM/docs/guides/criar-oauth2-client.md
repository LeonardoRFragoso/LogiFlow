# Criar OAuth2 Client via Interface Web

## Passo a Passo

1. **Acesse o SuiteCRM:**
   ```
   http://localhost:8080
   ```

2. **Faça login:**
   - Usuário: `admin`
   - Senha: `admin123`

3. **Acesse o módulo OAuth2:**
   
   **Opção A - Via Menu:**
   - Clique no menu superior (ícone de grade/9 pontos)
   - Procure por "OAuth2 Clients"
   - OU vá em "All" → "OAuth2 Clients"

   **Opção B - Via URL Direta:**
   ```
   http://localhost:8080/#OAuth2Clients
   ```

4. **Crie novo client:**
   - Clique em "Create OAuth2 Client"
   - Preencha:
     - **Name**: `LogiFlow Backend API`
     - **Is Confidential**: ✅ (marque)
     - **Allowed Grant Type**: `client_credentials`
   - **NÃO preencha Redirect URL** (deixe em branco para API)

5. **Salve e copie as credenciais:**
   - Clique em "Save"
   - O sistema vai gerar automaticamente:
     - **Client ID** (UUID)
     - **Client Secret** (string aleatória)
   
   ⚠️ **IMPORTANTE**: Copie AMBOS imediatamente!
   - Client ID: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
   - Client Secret: `xxxxxxxxxxxxxxxxxxxxxxxx`

6. **Atualize as configurações:**
   
   Edite o arquivo: `docker compose -f docker/docker-compose.yml.minimal.yml`
   
   Na seção `api: environment:`, atualize:
   ```yaml
   - SUITECRM_CLIENT_ID=<cole_o_client_id_aqui>
   - SUITECRM_CLIENT_SECRET=<cole_o_client_secret_aqui>
   ```

7. **Reinicie o container API:**
   ```bash
   docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.minimal.yml restart api
   ```

8. **Execute os testes:**
   ```bash
   .\testar-integracao-suitecrm.bat
   ```

---

## Se não conseguir acessar o módulo OAuth2

Execute este comando para verificar se o módulo existe:

```bash
docker exec logiflow_db mysql -ulogiflow -plogiflow123 logiflow_crm -e "SHOW TABLES LIKE 'oauth2%';"
```

Se as tabelas existirem mas o módulo não aparecer, pode ser que esteja oculto. Neste caso, volte aqui e me avise para tentarmos outra abordagem.
