# Gestão de Leads - Painel Admin

## 📋 Visão Geral

O sistema de gestão de leads permite que administradores visualizem, gerenciem e convertam solicitações de demonstração em clientes.

---

## 🎯 Funcionalidades Implementadas

### 1. **Listagem de Leads**
- ✅ Visualizar todos os leads de demonstração
- ✅ Filtrar por status (novo, contatado, qualificado, convertido, perdido)
- ✅ Filtrar por origem (site, indicação, google, facebook)
- ✅ Filtrar por vendedor atribuído
- ✅ Buscar por nome, email ou empresa
- ✅ Paginação

### 2. **Detalhes do Lead**
- ✅ Visualizar informações completas
- ✅ Histórico de alterações
- ✅ Dados de contato
- ✅ Mensagem/necessidade descrita

### 3. **Ações sobre Leads**
- ✅ Atualizar status
- ✅ Atribuir a vendedor
- ✅ Converter em cliente/tenant
- ✅ Adicionar notas
- ✅ Deletar lead

### 4. **Ações em Lote**
- ✅ Atribuir múltiplos leads
- ✅ Atualizar status de múltiplos leads

### 5. **Dashboard de Leads**
- ✅ Estatísticas gerais
- ✅ Taxa de conversão
- ✅ Leads por status
- ✅ Leads por origem

---

## 🔌 Endpoints da API

### **Base URL:** `/api/v1/admin/leads`

### 📊 **Listagem e Estatísticas**

#### 1. Listar Leads
```http
GET /api/v1/admin/leads/
Authorization: Bearer {token}

Query Parameters:
- status: string (opcional) - novo, contatado, qualificado, convertido, perdido
- source: string (opcional) - site, indicacao, google, facebook
- assigned_to: int (opcional) - ID do vendedor
- search: string (opcional) - busca por nome, email ou empresa
- limit: int (padrão: 50, máx: 100)
- offset: int (padrão: 0)

Response 200:
[
  {
    "id": 1,
    "name": "Leonardo Fragoso",
    "email": "leonardorfragoso@gmail.com",
    "phone": "(11) 99999-9999",
    "company": "Empresa Teste",
    "vehicles": "5",
    "message": "Quero conhecer o sistema",
    "status": "novo",
    "source": "site",
    "assigned_to": null,
    "created_at": "2026-03-11T20:41:37",
    "updated_at": "2026-03-11T20:41:37"
  }
]
```

#### 2. Estatísticas de Leads
```http
GET /api/v1/admin/leads/stats
Authorization: Bearer {token}

Response 200:
{
  "success": true,
  "data": {
    "total": 10,
    "por_status": {
      "novos": 5,
      "contatados": 2,
      "qualificados": 1,
      "convertidos": 1,
      "perdidos": 1
    },
    "por_origem": {
      "site": 8,
      "indicacao": 2
    },
    "taxa_conversao": 10.0
  }
}
```

#### 3. Detalhes do Lead
```http
GET /api/v1/admin/leads/{lead_id}
Authorization: Bearer {token}

Response 200:
{
  "id": 1,
  "name": "Leonardo Fragoso",
  "email": "leonardorfragoso@gmail.com",
  "phone": "(11) 99999-9999",
  "company": "Empresa Teste",
  "vehicles": "5",
  "message": "Quero conhecer o sistema",
  "status": "novo",
  "source": "site",
  "assigned_to": null,
  "created_at": "2026-03-11T20:41:37",
  "updated_at": "2026-03-11T20:41:37",
  "converted_at": null,
  "tenant_id": null
}
```

### ✏️ **Atualização**

#### 4. Atualizar Status
```http
PATCH /api/v1/admin/leads/{lead_id}/status
Authorization: Bearer {token}
Content-Type: application/json

Body:
{
  "status": "contatado",
  "observacao": "Cliente demonstrou interesse"
}

Response 200:
{
  "success": true,
  "message": "Status atualizado para contatado",
  "data": {
    "id": 1,
    "status": "contatado",
    "status_anterior": "novo"
  }
}
```

#### 5. Atribuir Lead a Vendedor
```http
PATCH /api/v1/admin/leads/{lead_id}/assign
Authorization: Bearer {token}
Content-Type: application/json

Body:
{
  "user_id": 2
}

Response 200:
{
  "success": true,
  "message": "Lead atribuído a João Silva",
  "data": {
    "id": 1,
    "assigned_to": 2,
    "assigned_to_name": "João Silva"
  }
}
```

### 🔄 **Conversão**

#### 6. Converter Lead em Cliente
```http
POST /api/v1/admin/leads/{lead_id}/convert
Authorization: Bearer {token}
Content-Type: application/json

Body:
{
  "create_tenant": true,
  "tenant_name": "Empresa Teste Ltda",
  "plan_type": "trial"
}

Response 200:
{
  "success": true,
  "message": "Lead convertido com sucesso",
  "data": {
    "lead_id": 1,
    "tenant_id": 5,
    "tenant_name": "Empresa Teste Ltda",
    "user_id": 10,
    "user_email": "leonardorfragoso@gmail.com",
    "senha_temporaria": "Abc123XyZ789",
    "plano": "trial"
  }
}
```

### 🗑️ **Exclusão**

#### 7. Deletar Lead
```http
DELETE /api/v1/admin/leads/{lead_id}
Authorization: Bearer {token}

Response 200:
{
  "success": true,
  "message": "Lead deletado com sucesso"
}
```

### 📦 **Ações em Lote**

#### 8. Atribuir Múltiplos Leads
```http
POST /api/v1/admin/leads/bulk/assign
Authorization: Bearer {token}
Content-Type: application/json

Body:
{
  "lead_ids": [1, 2, 3],
  "user_id": 2
}

Response 200:
{
  "success": true,
  "message": "3 leads atribuídos a João Silva",
  "count": 3
}
```

#### 9. Atualizar Status em Lote
```http
POST /api/v1/admin/leads/bulk/update-status
Authorization: Bearer {token}
Content-Type: application/json

Body:
{
  "lead_ids": [1, 2, 3],
  "status": "contatado"
}

Response 200:
{
  "success": true,
  "message": "3 leads atualizados para contatado",
  "count": 3
}
```

---

## 🎨 Implementação Frontend

### **Estrutura de Páginas Sugerida**

```
/admin
  /leads
    /index.tsx          - Lista de leads com filtros
    /[id].tsx           - Detalhes do lead
    /stats.tsx          - Dashboard de estatísticas
```

### **Componentes Necessários**

#### 1. **LeadsTable** - Tabela de Leads
```tsx
interface Lead {
  id: number;
  name: string;
  email: string;
  phone: string;
  company: string;
  vehicles?: string;
  message?: string;
  status: 'novo' | 'contatado' | 'qualificado' | 'convertido' | 'perdido';
  source: string;
  assigned_to?: number;
  created_at: string;
  updated_at: string;
}

// Colunas da tabela:
- ID
- Nome
- Empresa
- Email
- Telefone
- Status (badge colorido)
- Origem
- Atribuído a
- Data de criação
- Ações (botões: Ver, Editar, Atribuir, Converter, Deletar)
```

#### 2. **LeadFilters** - Filtros
```tsx
- Busca por nome/email/empresa
- Dropdown: Status
- Dropdown: Origem
- Dropdown: Vendedor
- Botão: Limpar filtros
```

#### 3. **LeadDetailModal** - Modal de Detalhes
```tsx
- Informações do lead
- Formulário para atualizar status
- Formulário para atribuir vendedor
- Botão para converter
- Histórico de ações
```

#### 4. **LeadStatsCards** - Cards de Estatísticas
```tsx
- Total de leads
- Leads novos
- Taxa de conversão
- Leads por origem (gráfico)
- Leads por status (gráfico)
```

#### 5. **ConvertLeadModal** - Modal de Conversão
```tsx
- Checkbox: Criar tenant?
- Input: Nome do tenant
- Select: Tipo de plano (trial, starter, professional, enterprise)
- Botão: Confirmar conversão
- Exibir credenciais geradas
```

### **Exemplo de Código React**

```tsx
// pages/admin/leads/index.tsx
import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';

export default function AdminLeadsPage() {
  const { token } = useAuth();
  const [leads, setLeads] = useState([]);
  const [filters, setFilters] = useState({
    status: '',
    source: '',
    search: ''
  });
  const [loading, setLoading] = useState(false);

  const fetchLeads = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.status) params.append('status', filters.status);
      if (filters.source) params.append('source', filters.source);
      if (filters.search) params.append('search', filters.search);

      const response = await fetch(
        `https://api.logiflow.com/api/v1/admin/leads/?${params}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      const data = await response.json();
      setLeads(data);
    } catch (error) {
      console.error('Erro ao carregar leads:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, [filters]);

  const handleUpdateStatus = async (leadId: number, newStatus: string) => {
    try {
      const response = await fetch(
        `https://api.logiflow.com/api/v1/admin/leads/${leadId}/status`,
        {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ status: newStatus })
        }
      );

      if (response.ok) {
        fetchLeads(); // Recarregar lista
        alert('Status atualizado com sucesso!');
      }
    } catch (error) {
      console.error('Erro ao atualizar status:', error);
    }
  };

  const handleConvert = async (leadId: number) => {
    try {
      const response = await fetch(
        `https://api.logiflow.com/api/v1/admin/leads/${leadId}/convert`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            create_tenant: true,
            plan_type: 'trial'
          })
        }
      );

      const data = await response.json();
      if (data.success) {
        alert(`Lead convertido! Senha temporária: ${data.data.senha_temporaria}`);
        fetchLeads();
      }
    } catch (error) {
      console.error('Erro ao converter lead:', error);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Gestão de Leads</h1>
      
      {/* Filtros */}
      <div className="mb-4 flex gap-4">
        <input
          type="text"
          placeholder="Buscar..."
          value={filters.search}
          onChange={(e) => setFilters({...filters, search: e.target.value})}
          className="border px-4 py-2 rounded"
        />
        
        <select
          value={filters.status}
          onChange={(e) => setFilters({...filters, status: e.target.value})}
          className="border px-4 py-2 rounded"
        >
          <option value="">Todos os status</option>
          <option value="novo">Novo</option>
          <option value="contatado">Contatado</option>
          <option value="qualificado">Qualificado</option>
          <option value="convertido">Convertido</option>
          <option value="perdido">Perdido</option>
        </select>
      </div>

      {/* Tabela */}
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2">ID</th>
            <th className="p-2">Nome</th>
            <th className="p-2">Empresa</th>
            <th className="p-2">Email</th>
            <th className="p-2">Status</th>
            <th className="p-2">Ações</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id} className="border-t">
              <td className="p-2">{lead.id}</td>
              <td className="p-2">{lead.name}</td>
              <td className="p-2">{lead.company}</td>
              <td className="p-2">{lead.email}</td>
              <td className="p-2">
                <span className={`px-2 py-1 rounded text-sm ${
                  lead.status === 'novo' ? 'bg-blue-100 text-blue-800' :
                  lead.status === 'convertido' ? 'bg-green-100 text-green-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {lead.status}
                </span>
              </td>
              <td className="p-2">
                <button
                  onClick={() => handleUpdateStatus(lead.id, 'contatado')}
                  className="bg-blue-500 text-white px-3 py-1 rounded mr-2"
                >
                  Contatar
                </button>
                <button
                  onClick={() => handleConvert(lead.id)}
                  className="bg-green-500 text-white px-3 py-1 rounded"
                >
                  Converter
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## 🎯 Fluxo de Trabalho Sugerido

### **1. Lead Novo Chega**
- ✅ Notificação aparece para admin
- ✅ Admin acessa `/admin/leads`
- ✅ Vê lead com status "novo"

### **2. Admin Qualifica o Lead**
- ✅ Clica em "Ver detalhes"
- ✅ Lê informações do lead
- ✅ Atualiza status para "contatado"
- ✅ Atribui a um vendedor

### **3. Vendedor Trabalha o Lead**
- ✅ Recebe notificação de atribuição
- ✅ Entra em contato com o lead
- ✅ Atualiza status para "qualificado"

### **4. Conversão**
- ✅ Admin clica em "Converter"
- ✅ Sistema cria tenant automaticamente
- ✅ Gera credenciais de acesso
- ✅ Admin envia credenciais para o cliente

---

## 📱 Onde Adicionar no Menu

Adicione no menu lateral do admin:

```tsx
{
  icon: "👥",
  label: "Leads",
  href: "/admin/leads",
  badge: countNovosLeads // Número de leads novos
}
```

---

## ✅ Checklist de Implementação

- [ ] Criar página `/admin/leads`
- [ ] Criar componente `LeadsTable`
- [ ] Criar componente `LeadFilters`
- [ ] Criar modal `LeadDetailModal`
- [ ] Criar modal `ConvertLeadModal`
- [ ] Criar página `/admin/leads/stats`
- [ ] Adicionar item no menu admin
- [ ] Testar todos os endpoints
- [ ] Adicionar loading states
- [ ] Adicionar error handling
- [ ] Adicionar confirmações para ações destrutivas

---

**O backend está 100% pronto! Basta implementar o frontend seguindo esta documentação.** 🎯
