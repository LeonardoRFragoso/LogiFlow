<template>
  <div class="configuracoes-fiscais-container">
    <div class="header">
      <h1>Configurações Fiscais</h1>
      <button @click="$router.back()" class="btn btn-secondary">
        <i class="icon-arrow-left"></i> Voltar
      </button>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando configurações...</p>
    </div>

    <form v-else @submit.prevent="salvarConfiguracoes" class="config-form">
      <div class="section">
        <h2>Dados do Emitente</h2>
        
        <div class="form-row">
          <div class="form-group">
            <label>CNPJ *</label>
            <input 
              type="text" 
              v-model="formData.emitente_cnpj" 
              class="form-control"
              placeholder="00.000.000/0000-00"
              required
            />
          </div>

          <div class="form-group">
            <label>Inscrição Estadual *</label>
            <input 
              type="text" 
              v-model="formData.emitente_ie" 
              class="form-control"
              required
            />
          </div>

          <div class="form-group">
            <label>Inscrição Municipal</label>
            <input 
              type="text" 
              v-model="formData.emitente_im" 
              class="form-control"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Razão Social *</label>
            <input 
              type="text" 
              v-model="formData.emitente_razao_social" 
              class="form-control"
              required
            />
          </div>

          <div class="form-group">
            <label>Nome Fantasia</label>
            <input 
              type="text" 
              v-model="formData.emitente_nome_fantasia" 
              class="form-control"
            />
          </div>
        </div>
      </div>

      <div class="section">
        <h2>Endereço do Emitente</h2>
        
        <div class="form-row">
          <div class="form-group" style="grid-column: 1 / -1;">
            <label>Endereço *</label>
            <input 
              type="text" 
              v-model="formData.emitente_endereco" 
              class="form-control"
              required
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Número *</label>
            <input 
              type="text" 
              v-model="formData.emitente_numero" 
              class="form-control"
              required
            />
          </div>

          <div class="form-group">
            <label>Complemento</label>
            <input 
              type="text" 
              v-model="formData.emitente_complemento" 
              class="form-control"
            />
          </div>

          <div class="form-group">
            <label>Bairro *</label>
            <input 
              type="text" 
              v-model="formData.emitente_bairro" 
              class="form-control"
              required
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Cidade *</label>
            <input 
              type="text" 
              v-model="formData.emitente_cidade" 
              class="form-control"
              required
            />
          </div>

          <div class="form-group">
            <label>UF *</label>
            <select v-model="formData.emitente_uf" class="form-control" required>
              <option value="">Selecione</option>
              <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
            </select>
          </div>

          <div class="form-group">
            <label>CEP *</label>
            <input 
              type="text" 
              v-model="formData.emitente_cep" 
              class="form-control"
              placeholder="00000-000"
              required
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Telefone</label>
            <input 
              type="text" 
              v-model="formData.emitente_telefone" 
              class="form-control"
              placeholder="(00) 0000-0000"
            />
          </div>

          <div class="form-group">
            <label>Email</label>
            <input 
              type="email" 
              v-model="formData.emitente_email" 
              class="form-control"
            />
          </div>
        </div>
      </div>

      <div class="section">
        <h2>Configurações de CT-e</h2>
        
        <div class="form-row">
          <div class="form-group">
            <label>Série Padrão</label>
            <input 
              type="text" 
              v-model="formData.cte_serie_padrao" 
              class="form-control"
            />
          </div>

          <div class="form-group">
            <label>Próximo Número</label>
            <input 
              type="number" 
              v-model.number="formData.cte_proximo_numero" 
              class="form-control"
              min="1"
            />
          </div>

          <div class="form-group">
            <label>Ambiente</label>
            <select v-model="formData.cte_ambiente" class="form-control">
              <option value="homologacao">Homologação</option>
              <option value="producao">Produção</option>
            </select>
          </div>
        </div>
      </div>

      <div class="section">
        <h2>Configurações de MDF-e</h2>
        
        <div class="form-row">
          <div class="form-group">
            <label>Série Padrão</label>
            <input 
              type="text" 
              v-model="formData.mdfe_serie_padrao" 
              class="form-control"
            />
          </div>

          <div class="form-group">
            <label>Próximo Número</label>
            <input 
              type="number" 
              v-model.number="formData.mdfe_proximo_numero" 
              class="form-control"
              min="1"
            />
          </div>

          <div class="form-group">
            <label>Ambiente</label>
            <select v-model="formData.mdfe_ambiente" class="form-control">
              <option value="homologacao">Homologação</option>
              <option value="producao">Produção</option>
            </select>
          </div>
        </div>
      </div>

      <div class="section">
        <h2>RNTRC e ANTT</h2>
        
        <div class="form-row">
          <div class="form-group">
            <label>RNTRC</label>
            <input 
              type="text" 
              v-model="formData.rntrc" 
              class="form-control"
              placeholder="Registro Nacional de Transportador de Cargas"
            />
          </div>

          <div class="form-group">
            <label>ANTT</label>
            <input 
              type="text" 
              v-model="formData.antt" 
              class="form-control"
            />
          </div>
        </div>
      </div>

      <div class="section">
        <h2>Integração Focus NFe</h2>
        
        <div class="alert alert-info">
          <strong>⚠️ Importante:</strong> A Focus NFe é uma API paga e externa. Você precisa contratar o serviço diretamente com a Focus NFe 
          (<a href="https://focusnfe.com.br" target="_blank">focusnfe.com.br</a>) e obter seu próprio Token de API no painel deles.
        </div>
        
        <div class="form-row">
          <div class="form-group" style="grid-column: 1 / -1;">
            <label>Seu Token Focus NFe *</label>
            <input 
              type="password" 
              v-model="formData.focusnfe_token" 
              class="form-control"
              placeholder="Cole aqui o token obtido no painel Focus NFe"
              required
            />
            <p class="hint">
              <strong>Onde obter:</strong> Acesse o painel Focus NFe → Minha Conta → Token de API
            </p>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Ambiente Focus NFe</label>
            <select v-model="formData.focusnfe_ambiente" class="form-control">
              <option value="homologacao">Homologação</option>
              <option value="producao">Produção</option>
            </select>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.focusnfe_ativo" />
              Integração Ativa
            </label>
          </div>
        </div>
      </div>

      <div class="section">
        <h2>Configurações de Emissão</h2>
        
        <div class="config-checkboxes">
          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.emitir_automatico_cte" />
            Emitir CT-e automaticamente ao aprovar pedido
          </label>

          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.agrupar_automatico_mdfe" />
            Agrupar CT-es em MDF-e automaticamente
          </label>

          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.enviar_email_apos_emissao" />
            Enviar email após emissão
          </label>

          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.enviar_whatsapp_apos_emissao" />
            Enviar WhatsApp após emissão
          </label>

          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.validar_dados_antes_emissao" />
            Validar dados antes da emissão
          </label>

          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.exigir_rntrc" />
            Exigir RNTRC na emissão
          </label>

          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.exigir_ciot" />
            Exigir CIOT na emissão
          </label>
        </div>
      </div>

      <div class="section">
        <h2>Observações Padrão</h2>
        
        <div class="form-group">
          <label>Observações CT-e</label>
          <textarea 
            v-model="formData.obs_padrao_cte" 
            rows="3"
            class="form-control"
            placeholder="Observações que aparecerão em todos os CT-es"
          ></textarea>
        </div>

        <div class="form-group">
          <label>Observações MDF-e</label>
          <textarea 
            v-model="formData.obs_padrao_mdfe" 
            rows="3"
            class="form-control"
            placeholder="Observações que aparecerão em todos os MDF-es"
          ></textarea>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="salvando" class="btn btn-primary btn-lg">
          <span v-if="salvando">Salvando...</span>
          <span v-else>Salvar Configurações</span>
        </button>
        <button type="button" @click="$router.back()" class="btn btn-secondary btn-lg">
          Cancelar
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const loading = ref(true)
const salvando = ref(false)

const formData = ref({
  emitente_cnpj: '',
  emitente_razao_social: '',
  emitente_nome_fantasia: '',
  emitente_ie: '',
  emitente_im: '',
  emitente_endereco: '',
  emitente_numero: '',
  emitente_complemento: '',
  emitente_bairro: '',
  emitente_cidade: '',
  emitente_uf: '',
  emitente_cep: '',
  emitente_telefone: '',
  emitente_email: '',
  cte_serie_padrao: '1',
  cte_proximo_numero: 1,
  cte_ambiente: 'homologacao',
  mdfe_serie_padrao: '1',
  mdfe_proximo_numero: 1,
  mdfe_ambiente: 'homologacao',
  rntrc: '',
  antt: '',
  focusnfe_token: '',
  focusnfe_ambiente: 'homologacao',
  focusnfe_ativo: false,
  emitir_automatico_cte: false,
  agrupar_automatico_mdfe: false,
  enviar_email_apos_emissao: true,
  enviar_whatsapp_apos_emissao: false,
  validar_dados_antes_emissao: true,
  exigir_rntrc: true,
  exigir_ciot: false,
  obs_padrao_cte: '',
  obs_padrao_mdfe: ''
})

const ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

async function carregarConfiguracoes() {
  loading.value = true
  try {
    const response = await api.get('/fiscal/configuracao')
    
    if (response.data.data) {
      Object.assign(formData.value, response.data.data)
    }
  } catch (error) {
    console.error('Erro ao carregar configurações:', error)
  } finally {
    loading.value = false
  }
}

async function salvarConfiguracoes() {
  salvando.value = true
  try {
    await api.post('/fiscal/configuracao', formData.value)
    alert('Configurações salvas com sucesso!')
    router.back()
  } catch (error) {
    console.error('Erro ao salvar configurações:', error)
    alert(error.response?.data?.detail || 'Erro ao salvar configurações')
  } finally {
    salvando.value = false
  }
}

onMounted(() => {
  carregarConfiguracoes()
})
</script>

<style scoped>
.configuracoes-fiscais-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  color: #333;
}

.loading {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.config-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.section {
  padding: 30px;
  border-bottom: 1px solid #e9ecef;
}

.section:last-child {
  border-bottom: none;
}

.section h2 {
  font-size: 20px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #007bff;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #495057;
}

.form-control {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: #007bff;
}

textarea.form-control {
  resize: vertical;
  font-family: inherit;
}

.hint {
  font-size: 12px;
  color: #6c757d;
  margin: 0;
}

.alert {
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
  border: 1px solid;
}

.alert-info {
  background: #d1ecf1;
  color: #0c5460;
  border-color: #bee5eb;
}

.alert strong {
  font-weight: 600;
}

.alert a {
  color: #0c5460;
  text-decoration: underline;
  font-weight: 600;
}

.config-checkboxes {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #495057;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding: 30px;
  background: #f8f9fa;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-lg {
  padding: 12px 32px;
  font-size: 16px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
