# LogiFlow CRM - Helm Chart

Helm chart para deployment do LogiFlow CRM em Kubernetes.

## 📋 Pré-requisitos

- Kubernetes 1.24+
- Helm 3.10+
- kubectl configurado
- Ingress Controller (nginx recomendado)
- cert-manager (para SSL/TLS)

### Instalar Dependências

```bash
# Ingress Nginx
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace

# Cert-Manager
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true
```

## 🚀 Deployment

### 1. Staging Environment

```bash
# Adicionar repositório (quando disponível)
helm repo add logiflow https://charts.logiflow.com
helm repo update

# Instalar em staging
helm install logiflow-staging logiflow/logiflow \
  -f helm/logiflow/values-staging.yaml \
  --namespace logiflow-staging \
  --create-namespace

# Ou localmente
helm install logiflow-staging ./helm/logiflow \
  -f ./helm/logiflow/values-staging.yaml \
  --namespace logiflow-staging \
  --create-namespace
```

### 2. Production Environment

```bash
# Criar namespace
kubectl create namespace logiflow-production

# Instalar secrets (IMPORTANTE!)
kubectl create secret generic logiflow-secrets \
  --from-literal=database-url=postgresql://user:pass@host/db \
  --from-literal=redis-url=redis://:password@host:6379/0 \
  --from-literal=secret-key=<GERAR-SECRETO> \
  --from-literal=sendgrid-api-key=SG_... \
  --from-literal=google-api-key=AIza... \
  --namespace logiflow-production

# Deploy
helm install logiflow-prod ./helm/logiflow \
  -f ./helm/logiflow/values-production.yaml \
  --namespace logiflow-production \
  --set global.domain=logiflow.com
```

## 📊 Verificar Deployment

```bash
# Status dos pods
kubectl get pods -n logiflow-staging
kubectl get svc -n logiflow-staging
kubectl get ingress -n logiflow-staging

# Logs
kubectl logs -n logiflow-staging deployment/logiflow-staging-backend
kubectl logs -n logiflow-staging deployment/logiflow-staging-frontend

# Acesso ao Grafana
kubectl port-forward -n logiflow-staging svc/logiflow-grafana 3000:3000
# browser: http://localhost:3000

# Acesso ao Prometheus
kubectl port-forward -n logiflow-staging svc/logiflow-prometheus 9090:9090
# browser: http://localhost:9090
```

## 🔧 Configuração

### Customizar Values

```bash
# Staging - 2 replicas
helm upgrade logiflow-staging ./helm/logiflow \
  -f ./helm/logiflow/values-staging.yaml \
  --set backend.replicaCount=3 \
  --namespace logiflow-staging

# Production - 5 replicas
helm upgrade logiflow-prod ./helm/logiflow \
  -f ./helm/logiflow/values-production.yaml \
  --set backend.autoscaling.maxReplicas=10 \
  --namespace logiflow-production
```

### Atualizar Imagens

```bash
# Backend apenas
helm upgrade logiflow-prod ./helm/logiflow \
  -f ./helm/logiflow/values-production.yaml \
  --set backend.image.tag=v1.2.0 \
  --namespace logiflow-production

# Frontend apenas
helm upgrade logiflow-prod ./helm/logiflow \
  -f ./helm/logiflow/values-production.yaml \
  --set frontend.image.tag=v1.2.0 \
  --namespace logiflow-production
```

## 📈 Escalabilidade

### Auto-scaling

HPA (Horizontal Pod Autoscaler) é automático:

```bash
# Monitorar auto-scaling
kubectl get hpa -n logiflow-production -w

# Metrics
kubectl get --raw /apis/custom.metrics.k8s.io
```

### Manual Scaling

```bash
# Aumentar backend replicas
kubectl scale deployment logiflow-prod-backend \
  --replicas=5 \
  -n logiflow-production

# Verificar
kubectl get deployment -n logiflow-production
```

## 🔐 Segurança

### Secrets Management

```bash
# Opção 1: Sealed Secrets
helm repo add sealedsecrets https://kontena.github.io/sealedsecrets
helm install sealed-secrets sealedsecrets/sealed-secrets \
  --namespace kube-system

# Opção 2: External Secrets (AWS, Vault)
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets-system \
  --create-namespace

# Opção 3: AWS Secrets Manager
# Configure IAM role for pods
```

### Network Policies

```bash
# Enable network policies (production only)
helm upgrade logiflow-prod ./helm/logiflow \
  -f ./helm/logiflow/values-production.yaml \
  --set networkPolicy.enabled=true \
  --namespace logiflow-production
```

## 🚨 Troubleshooting

### Pods não iniciando

```bash
# Descrição detalhada
kubectl describe pod -n logiflow-staging <pod-name>

# Logs completos
kubectl logs -n logiflow-staging <pod-name> --previous

# Debug shell
kubectl debug -n logiflow-staging <pod-name> -it --image=busybox
```

### Banco de dados não conectando

```bash
# Testar conectividade
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql postgresql://user:pass@db-service:5432/logiflow

# Verificar secrets
kubectl get secrets -n logiflow-staging
kubectl describe secret logiflow-secrets -n logiflow-staging
```

### Ingress não rotando

```bash
# Verificar ingress
kubectl get ingress -n logiflow-staging
kubectl describe ingress logiflow-staging-frontend -n logiflow-staging

# Testar DNS
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  nslookup api.logiflow.com
```

## 📦 Backup & Restore

### Backup Database

```bash
# Pod exec backup
kubectl exec -n logiflow-prod <postgres-pod> -- \
  pg_dump -U logiflow logiflow_prod > backup.sql

# Ou manutenção automática no values-production.yaml
```

### Restore Database

```bash
kubectl exec -i -n logiflow-prod <postgres-pod> -- \
  psql -U logiflow logiflow_prod < backup.sql
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/helm-deploy.yml
name: Helm Deploy
on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Kubernetes
        run: |
          helm upgrade --install logiflow ./helm/logiflow \
            -f ./helm/logiflow/values-production.yaml \
            --kubeconfig=${{ secrets.KUBECONFIG }}
```

## 📊 Monitoramento

Métricas disponíveis automaticamente:

- Prometheus: `:9090/metrics`
- Grafana: `:3000` (dashboards pré-configurados)
- API health: `/health`
- API readiness: `/ready`

## 🛠️ Manutenção

### Upgrade de Versão

```bash
# Dry-run
helm upgrade logiflow-prod ./helm/logiflow \
  -f ./helm/logiflow/values-production.yaml \
  --dry-run --debug

# Actual upgrade (rolling)
helm upgrade logiflow-prod ./helm/logiflow \
  -f ./helm/logiflow/values-production.yaml

# Rollback se necessário
helm rollback logiflow-prod 1
```

### Limpeza

```bash
# Listar releases
helm list -n logiflow-staging

# Desinstalar
helm uninstall logiflow-staging -n logiflow-staging

# Deletar namespace
kubectl delete namespace logiflow-staging
```

## 📚 Estrutura

```
helm/logiflow/
├── Chart.yaml                    # Metadados
├── values.yaml                   # Valores default (dev)
├── values-staging.yaml           # Valores staging
├── values-production.yaml        # Valores production
└── templates/
    ├── _helpers.tpl             # Templates helpers
    ├── deployment-backend.yaml   # Backend deployment
    ├── deployment-frontend.yaml  # Frontend deployment
    ├── service.yaml             # Services
    ├── ingress.yaml             # Ingress rules
    ├── hpa.yaml                 # Auto-scaling
    ├── pdb.yaml                 # Pod disruption budget
    ├── configmap.yaml           # ConfigMaps
    └── serviceaccount.yaml      # RBAC
```

## 🎯 Best Practices

1. ✅ **Use image tags específicas** em produção (não `latest`)
2. ✅ **Configure resource limits** para evitar crashes
3. ✅ **Enable PDB** para evitar downtime durante updates
4. ✅ **Use network policies** para segurança
5. ✅ **Configure health checks** (liveness + readiness)
6. ✅ **Enable auto-scaling** com métricas apropriadas
7. ✅ **Backup automático** de database
8. ✅ **Monitoramento ativo** com alertas

## 📞 Suporte

- Documentação: https://github.com/LeonardoRFragoso/LogiFlow
- Issues: https://github.com/LeonardoRFragoso/LogiFlow/issues
- Email: devops@logiflow.com
