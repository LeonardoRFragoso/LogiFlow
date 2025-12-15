# 📱 LogiFlow - Guia dos Apps

Documentação completa dos aplicativos **App do Motorista (PWA)** e **Portal do Cliente (Tracking)**.

---

## 📦 App do Motorista (PWA)

### 🎯 Funcionalidades

- ✅ **Login Seguro** - Autenticação JWT
- 📦 **Lista de Entregas** - Visualização de entregas ativas e concluídas
- 📍 **GPS Integrado** - Compartilhamento de localização em tempo real
- ✏️ **Atualização de Status** - Alterar status das entregas
- 📷 **Captura de Fotos** - Comprovantes de entrega
- 🔔 **Notificações Push** - Alertas de novas entregas
- 💼 **Modo Offline** - Funciona sem internet

### 🚀 Executar em Desenvolvimento

```bash
cd "LogiFlow CRM/app-motorista"
npm install
npm run dev
```

Acesse: `http://localhost:5174`

### 📦 Build para Produção

```bash
npm run build
npm run preview  # Preview do build
```

### 📱 Instalar como PWA

1. Abra o app no navegador mobile
2. Chrome: Menu → "Adicionar à tela inicial"
3. Safari (iOS): Compartilhar → "Adicionar à Tela de Início"

### 🔑 Credenciais de Teste

```
Usuário: motorista@logiflow.com
Senha: motorista123
```

### 📊 Estrutura do Projeto

```
app-motorista/
├── public/
│   ├── manifest.json      # Configuração PWA
│   ├── sw.js              # Service Worker
│   └── icons/             # Ícones do app
├── src/
│   ├── views/
│   │   ├── HomeView.vue           # Dashboard
│   │   ├── EntregasView.vue       # Lista de entregas
│   │   ├── EntregaDetalheView.vue # Detalhes
│   │   ├── AtualizarStatusView.vue # Alterar status
│   │   ├── OcorrenciaView.vue     # Registrar ocorrências
│   │   ├── PerfilView.vue         # Perfil do motorista
│   │   └── LoginView.vue          # Login
│   ├── stores/
│   │   ├── auth.js        # Autenticação
│   │   └── entregas.js    # Gestão de entregas
│   ├── services/
│   │   └── api.js         # Cliente HTTP
│   └── router/
│       └── index.js       # Rotas
├── package.json
└── vite.config.js
```

### 🔧 Configuração da API

Edite `src/services/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
```

Crie `.env.local`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

## 🌐 Portal do Cliente (Tracking)

### 🎯 Funcionalidades

- 🔍 **Rastreamento** - Busca por código de entrega
- 🗺️ **Mapa Interativo** - Localização em tempo real
- 📊 **Timeline** - Histórico completo de status
- 🔔 **Notificações WhatsApp** - Cadastro para receber atualizações
- 📤 **Compartilhamento** - Compartilhar status da entrega
- 🖨️ **Impressão** - Imprimir comprovante
- 📱 **PWA** - Pode ser instalado como app

### 🚀 Executar em Desenvolvimento

```bash
cd "LogiFlow CRM/portal-cliente"
npm install
npm run dev
```

Acesse: `http://localhost:5175`

### 📦 Build para Produção

```bash
npm run build
npm run preview  # Preview do build
```

### 🔍 Como Usar

1. Acesse o portal
2. Digite o código de rastreamento (ex: `ENT-2024-001`)
3. Clique em "Rastrear"
4. Visualize status, mapa e timeline
5. Opcional: Cadastre WhatsApp para notificações

### 🧪 Códigos de Teste

- `ENT-2024-001` - Entrega em trânsito
- `ENT-2024-002` - Saiu para entrega
- `ENT-2024-003` - Aguardando coleta

### 📊 Estrutura do Projeto

```
portal-cliente/
├── public/
│   ├── manifest.json      # Configuração PWA
│   ├── sw.js              # Service Worker
│   └── icons/             # Ícones do portal
├── src/
│   ├── views/
│   │   ├── HomeView.vue       # Busca de rastreamento
│   │   └── TrackingView.vue   # Resultado do rastreamento
│   ├── router.js          # Rotas
│   ├── App.vue            # App principal
│   └── main.js            # Entry point
├── package.json
└── vite.config.js
```

### 🔧 Configuração da API

Crie `.env.local`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

## 🐳 Docker - Executar Ambos os Apps

### docker-compose.yml

Adicione ao `docker-compose.yml`:

```yaml
  # App do Motorista
  app-motorista:
    build:
      context: ./app-motorista
      dockerfile: ../docker/app-motorista/Dockerfile
    container_name: logiflow_app_motorista
    restart: unless-stopped
    ports:
      - "5174:80"
    environment:
      - VITE_API_URL=http://api:8000/api/v1
    networks:
      - logiflow_network

  # Portal do Cliente
  portal-cliente:
    build:
      context: ./portal-cliente
      dockerfile: ../docker/portal-cliente/Dockerfile
    container_name: logiflow_portal_cliente
    restart: unless-stopped
    ports:
      - "5175:80"
    environment:
      - VITE_API_URL=http://api:8000/api/v1
    networks:
      - logiflow_network
```

### Dockerfile (Ambos)

Crie `docker/app-motorista/Dockerfile`:

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://api:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Executar com Docker

```bash
docker-compose up -d app-motorista portal-cliente
```

**Acessos**:
- App Motorista: `http://localhost:5174`
- Portal Cliente: `http://localhost:5175`

---

## 🔐 API Backend - Endpoints

### Para o App do Motorista

```http
POST   /api/v1/auth/login                    # Login
POST   /api/v1/auth/refresh                  # Refresh token
GET    /api/v1/entregas                      # Listar entregas
GET    /api/v1/entregas/{id}                 # Detalhes da entrega
PATCH  /api/v1/entregas/{id}/status          # Atualizar status
POST   /api/v1/entregas/{id}/ocorrencia      # Registrar ocorrência
POST   /api/v1/entregas/{id}/foto            # Upload de foto
POST   /api/v1/motoristas/localizacao        # Enviar localização GPS
GET    /api/v1/motoristas/perfil             # Perfil do motorista
```

### Para o Portal do Cliente

```http
GET    /api/v1/entregas/rastrear/{codigo}    # Rastrear entrega
GET    /api/v1/entregas/{id}/timeline        # Histórico de status
POST   /api/v1/entregas/{id}/notificar       # Cadastrar WhatsApp
```

---

## 📊 Métricas e Monitoramento

### Service Worker Status

```javascript
// No console do navegador
navigator.serviceWorker.getRegistrations()
  .then(regs => console.log(regs))
```

### Cache Status

```javascript
caches.keys().then(keys => console.log(keys))
```

### Notificações (App Motorista)

```javascript
Notification.requestPermission()
  .then(permission => console.log(permission))
```

---

## 🐛 Troubleshooting

### App não instala como PWA

**Causa**: Manifest ou Service Worker com erro

**Solução**:
1. Abra DevTools → Application → Manifest
2. Verifique erros
3. Certifique-se que está em HTTPS (ou localhost)

### Service Worker não atualiza

**Solução**:
```javascript
// No console
navigator.serviceWorker.getRegistrations()
  .then(regs => regs.forEach(reg => reg.unregister()))
```

### API não responde (CORS)

**Causa**: Configuração CORS no backend

**Solução**: No `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Build falha

**Solução**:
```bash
# Limpar cache
rm -rf node_modules dist
npm install
npm run build
```

---

## 🚀 Deploy em Produção

### Netlify / Vercel

1. Conecte o repositório
2. Configure build:
   - Build command: `npm run build`
   - Publish directory: `dist`
3. Adicione variáveis de ambiente:
   - `VITE_API_URL=https://api.logiflow.com.br/api/v1`

### Nginx (VPS)

```bash
# Build local
npm run build

# Upload
scp -r dist/* user@server:/var/www/app-motorista/

# Configurar Nginx
sudo nano /etc/nginx/sites-available/app-motorista

# Reload Nginx
sudo nginx -t && sudo systemctl reload nginx
```

### SSL (Let's Encrypt)

```bash
sudo certbot --nginx -d app.logiflow.com.br
sudo certbot --nginx -d portal.logiflow.com.br
```

---

## 📚 Recursos Adicionais

- [PWA Checklist](https://web.dev/pwa-checklist/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)
- [Push Notifications](https://web.dev/push-notifications-overview/)

---

## ✅ Checklist de Implantação

### App do Motorista
- [ ] Configurado `.env` com URL da API
- [ ] Service Worker registrado e funcionando
- [ ] Manifest válido
- [ ] Ícones PWA gerados (192x192, 512x512)
- [ ] Login funcionando
- [ ] Entregas carregando
- [ ] GPS capturando localização
- [ ] Notificações ativadas
- [ ] Testado modo offline

### Portal do Cliente
- [ ] Configurado `.env` com URL da API
- [ ] Service Worker registrado
- [ ] Manifest válido
- [ ] Busca de rastreamento funcionando
- [ ] Mapa exibindo localização
- [ ] Timeline mostrando histórico
- [ ] WhatsApp cadastrando
- [ ] Compartilhamento funcionando
- [ ] Impressão formatada

---

**Última atualização**: 2024-12-15  
**Versão**: 1.0.0

