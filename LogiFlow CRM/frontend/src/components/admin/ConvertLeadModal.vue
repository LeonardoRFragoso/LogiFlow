<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- Header -->
      <div class="modal-header">
        <div>
          <h2 class="modal-title">Converter Lead em Cliente</h2>
          <p class="modal-subtitle">{{ lead.name }} - {{ lead.company }}</p>
        </div>
        <button @click="$emit('close')" class="btn-close">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- Body -->
      <div class="modal-body">
        <div v-if="!converted">
          <!-- Informações do Lead -->
          <div class="lead-info">
            <div class="info-row">
              <span class="label">Email:</span>
              <span class="value">{{ lead.email }}</span>
            </div>
            <div class="info-row">
              <span class="label">Telefone:</span>
              <span class="value">{{ lead.phone }}</span>
            </div>
            <div class="info-row">
              <span class="label">Veículos:</span>
              <span class="value">{{ lead.vehicles || 'Não informado' }}</span>
            </div>
          </div>

          <!-- Opções de Conversão -->
          <div class="form-section">
            <div class="form-group">
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="formData.create_tenant"
                  class="checkbox-input"
                />
                <span>Criar tenant (conta) automaticamente</span>
              </label>
              <p class="help-text">
                Ao marcar esta opção, será criado automaticamente um tenant e um usuário admin para o cliente.
              </p>
            </div>

            <div v-if="formData.create_tenant" class="tenant-options">
              <div class="form-group">
                <label>Nome do Tenant</label>
                <input
                  v-model="formData.tenant_name"
                  type="text"
                  class="form-input"
                  :placeholder="lead.company"
                />
                <p class="help-text">Deixe em branco para usar o nome da empresa</p>
              </div>

              <div class="form-group">
                <label>Tipo de Plano</label>
                <select v-model="formData.plan_type" class="form-select">
                  <option value="trial">Trial (Teste Grátis - 14 dias)</option>
                  <option value="starter">Starter (Básico)</option>
                  <option value="professional">Professional (Profissional)</option>
                  <option value="enterprise">Enterprise (Empresarial)</option>
                </select>
              </div>

              <div class="plan-info">
                <i class="fas fa-info-circle"></i>
                <div>
                  <p class="plan-info-title">{{ getPlanInfo().title }}</p>
                  <p class="plan-info-desc">{{ getPlanInfo().description }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Aviso -->
          <div class="warning-box">
            <i class="fas fa-exclamation-triangle"></i>
            <div>
              <p class="warning-title">Atenção!</p>
              <p class="warning-text">
                Esta ação irá marcar o lead como "Convertido" e não poderá ser desfeita.
                {{ formData.create_tenant ? 'Um email com as credenciais de acesso será gerado.' : '' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Resultado da Conversão -->
        <div v-else class="success-result">
          <div class="success-icon">
            <i class="fas fa-check-circle"></i>
          </div>
          <h3 class="success-title">Lead Convertido com Sucesso!</h3>
          
          <div v-if="conversionResult.tenant_id" class="credentials-box">
            <h4 class="credentials-title">
              <i class="fas fa-key"></i>
              Credenciais de Acesso
            </h4>
            <div class="credentials-grid">
              <div class="credential-item">
                <label>Tenant ID</label>
                <div class="credential-value">
                  <code>{{ conversionResult.tenant_id }}</code>
                  <button @click="copyToClipboard(conversionResult.tenant_id)" class="btn-copy">
                    <i class="fas fa-copy"></i>
                  </button>
                </div>
              </div>
              <div class="credential-item">
                <label>Nome do Tenant</label>
                <div class="credential-value">
                  <code>{{ conversionResult.tenant_name }}</code>
                  <button @click="copyToClipboard(conversionResult.tenant_name)" class="btn-copy">
                    <i class="fas fa-copy"></i>
                  </button>
                </div>
              </div>
              <div class="credential-item">
                <label>Email de Acesso</label>
                <div class="credential-value">
                  <code>{{ conversionResult.user_email }}</code>
                  <button @click="copyToClipboard(conversionResult.user_email)" class="btn-copy">
                    <i class="fas fa-copy"></i>
                  </button>
                </div>
              </div>
              <div class="credential-item">
                <label>Senha Temporária</label>
                <div class="credential-value">
                  <code class="password">{{ conversionResult.senha_temporaria }}</code>
                  <button @click="copyToClipboard(conversionResult.senha_temporaria)" class="btn-copy">
                    <i class="fas fa-copy"></i>
                  </button>
                </div>
              </div>
              <div class="credential-item">
                <label>Plano</label>
                <div class="credential-value">
                  <code>{{ conversionResult.plano }}</code>
                </div>
              </div>
            </div>
            
            <div class="alert-info">
              <i class="fas fa-info-circle"></i>
              <p>
                <strong>Importante:</strong> Copie estas credenciais e envie para o cliente.
                A senha temporária deve ser alterada no primeiro acesso.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="modal-footer">
        <button
          v-if="!converted"
          @click="$emit('close')"
          class="btn-secondary"
        >
          Cancelar
        </button>
        <button
          v-if="!converted"
          @click="convertLead"
          :disabled="loading"
          class="btn-primary"
        >
          <i class="fas fa-spinner fa-spin" v-if="loading"></i>
          <i class="fas fa-check-circle" v-else></i>
          {{ loading ? 'Convertendo...' : 'Confirmar Conversão' }}
        </button>
        <button
          v-if="converted"
          @click="handleClose"
          class="btn-primary"
        >
          Fechar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'ConvertLeadModal',
  props: {
    lead: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'converted'],
  setup(props, { emit }) {
    const authStore = useAuthStore();
    const loading = ref(false);
    const converted = ref(false);
    const conversionResult = ref(null);

    const formData = reactive({
      create_tenant: true,
      tenant_name: '',
      plan_type: 'trial'
    });

    const convertLead = async () => {
      loading.value = true;
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/v1/admin/leads/${props.lead.id}/convert`,
          {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${authStore.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
          }
        );

        const data = await response.json();

        if (response.ok && data.success) {
          converted.value = true;
          conversionResult.value = data.data;
        } else {
          alert(data.message || 'Erro ao converter lead');
        }
      } catch (error) {
        console.error('Erro ao converter lead:', error);
        alert('Erro ao converter lead');
      } finally {
        loading.value = false;
      }
    };

    const getPlanInfo = () => {
      const plans = {
        trial: {
          title: 'Trial - Teste Grátis',
          description: '14 dias de acesso completo sem custo'
        },
        starter: {
          title: 'Starter - Plano Básico',
          description: 'Ideal para pequenas empresas iniciando'
        },
        professional: {
          title: 'Professional - Plano Profissional',
          description: 'Recursos avançados para empresas em crescimento'
        },
        enterprise: {
          title: 'Enterprise - Plano Empresarial',
          description: 'Solução completa para grandes operações'
        }
      };
      return plans[formData.plan_type] || plans.trial;
    };

    const copyToClipboard = async (text) => {
      try {
        await navigator.clipboard.writeText(text);
        alert('Copiado para a área de transferência!');
      } catch (error) {
        console.error('Erro ao copiar:', error);
        alert('Erro ao copiar');
      }
    };

    const handleClose = () => {
      emit('converted');
      emit('close');
    };

    return {
      loading,
      converted,
      conversionResult,
      formData,
      convertLead,
      getPlanInfo,
      copyToClipboard,
      handleClose
    };
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
}

.modal-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.btn-close {
  padding: 0.5rem;
  background: #f3f4f6;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #e5e7eb;
  color: #111827;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.lead-info {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: #6b7280;
  font-size: 0.875rem;
}

.value {
  color: #111827;
  font-size: 0.875rem;
}

.form-section {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  font-weight: 500;
}

.checkbox-input {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
}

.help-text {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.form-input,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  ring: 2px;
  ring-color: #3b82f620;
}

.tenant-options {
  padding-left: 2rem;
  margin-top: 1rem;
}

.plan-info {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: #eff6ff;
  border-radius: 0.5rem;
  border-left: 4px solid #3b82f6;
}

.plan-info i {
  color: #3b82f6;
  font-size: 1.25rem;
}

.plan-info-title {
  font-weight: 600;
  color: #1e40af;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.plan-info-desc {
  font-size: 0.75rem;
  color: #1e40af;
}

.warning-box {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: #fef3c7;
  border-radius: 0.5rem;
  border-left: 4px solid #f59e0b;
}

.warning-box i {
  color: #f59e0b;
  font-size: 1.25rem;
}

.warning-title {
  font-weight: 600;
  color: #92400e;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.warning-text {
  font-size: 0.75rem;
  color: #92400e;
}

.success-result {
  text-align: center;
}

.success-icon {
  font-size: 4rem;
  color: #10b981;
  margin-bottom: 1rem;
}

.success-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 1.5rem;
}

.credentials-box {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 0.75rem;
  text-align: left;
  margin-top: 1.5rem;
}

.credentials-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.credentials-grid {
  display: grid;
  gap: 1rem;
  margin-bottom: 1rem;
}

.credential-item label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.credential-value {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.credential-value code {
  flex: 1;
  padding: 0.75rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  color: #111827;
}

.credential-value code.password {
  font-weight: 700;
  color: #dc2626;
}

.btn-copy {
  padding: 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-copy:hover {
  background: #2563eb;
}

.alert-info {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: #dbeafe;
  border-radius: 0.5rem;
  margin-top: 1rem;
}

.alert-info i {
  color: #1e40af;
  font-size: 1.25rem;
}

.alert-info p {
  font-size: 0.75rem;
  color: #1e40af;
  line-height: 1.5;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #059669;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
