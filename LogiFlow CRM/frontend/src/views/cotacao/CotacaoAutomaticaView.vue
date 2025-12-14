<template>
  <div class="cotacao-automatica">
    <div class="page-header">
      <h1>💰 Cotação Automática</h1>
      <p>Compare preços de múltiplas transportadoras e encontre a melhor opção</p>
    </div>

    <!-- Formulário de Cotação -->
    <div class="cotacao-form-card">
      <h2>📦 Dados da Cotação</h2>
      
      <form @submit.prevent="cotar" class="cotacao-form">
        <div class="form-row">
          <div class="form-group">
            <label>CEP Origem *</label>
            <input 
              v-model="form.origem_cep" 
              type="text" 
              class="form-control" 
              placeholder="00000-000"
              maxlength="9"
              required
            >
          </div>

          <div class="form-group">
            <label>CEP Destino *</label>
            <input 
              v-model="form.destino_cep" 
              type="text" 
              class="form-control" 
              placeholder="00000-000"
              maxlength="9"
              required
            >
          </div>

          <div class="form-group">
            <label>Peso (kg) *</label>
            <input 
              v-model.number="form.peso_kg" 
              type="number" 
              class="form-control" 
              placeholder="0.0"
              step="0.1"
              min="0.1"
              required
            >
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Altura (cm)</label>
            <input 
              v-model.number="form.altura_cm" 
              type="number" 
              class="form-control" 
              placeholder="20"
              min="1"
            >
          </div>

          <div class="form-group">
            <label>Largura (cm)</label>
            <input 
              v-model.number="form.largura_cm" 
              type="number" 
              class="form-control" 
              placeholder="20"
              min="1"
            >
          </div>

          <div class="form-group">
            <label>Comprimento (cm)</label>
            <input 
              v-model.number="form.comprimento_cm" 
              type="number" 
              class="form-control" 
              placeholder="20"
              min="1"
            >
          </div>

          <div class="form-group">
            <label>Valor da Mercadoria (R$)</label>
            <input 
              v-model.number="form.valor_mercadoria" 
              type="number" 
              class="form-control" 
              placeholder="0.00"
              step="0.01"
              min="0"
            >
          </div>
        </div>

        <div class="form-row">
          <div class="form-group checkbox-group">
            <label>
              <input type="checkbox" v-model="form.incluir_melhor_envio">
              Incluir Melhor Envio
            </label>
          </div>

          <div class="form-group checkbox-group">
            <label>
              <input type="checkbox" v-model="form.incluir_frenet">
              Incluir Frenet
            </label>
          </div>

          <div class="form-group checkbox-group">
            <label>
              <input type="checkbox" v-model="form.incluir_tabela_propria">
              Incluir Tabela Própria
            </label>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="loading">
            <span v-if="!loading">🔍 Cotar Frete</span>
            <span v-else>⏳ Cotando...</span>
          </button>
          <button type="button" @click="limparForm" class="btn-secondary">
            🗑️ Limpar
          </button>
        </div>
      </form>
    </div>

    <!-- Resultados -->
    <div v-if="resultado" class="resultados-section">
      <!-- Resumo -->
      <div class="resumo-card">
        <div class="resumo-header">
          <h2>✅ Cotação Realizada</h2>
          <span class="total-cotacoes">{{ resultado.total_cotacoes }} opções encontradas</span>
        </div>

        <div v-if="resultado.melhor_opcao" class="melhor-opcao">
          <div class="melhor-badge">⭐ MELHOR OPÇÃO</div>
          <div class="melhor-content">
            <h3>{{ resultado.melhor_opcao.transportadora }} - {{ resultado.melhor_opcao.servico }}</h3>
            <div class="melhor-stats">
              <div class="stat">
                <span class="label">Valor:</span>
                <span class="value">R$ {{ resultado.melhor_opcao.valor.toFixed(2) }}</span>
              </div>
              <div class="stat">
                <span class="label">Prazo:</span>
                <span class="value">{{ resultado.melhor_opcao.prazo_dias }} dias úteis</span>
              </div>
              <div class="stat">
                <span class="label">Fonte:</span>
                <span class="value">{{ fonteLabel(resultado.melhor_opcao.fonte) }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="resultado.economia && resultado.economia.valor > 0" class="economia-card">
          <div class="economia-icon">💰</div>
          <div class="economia-content">
            <h4>Economia Identificada</h4>
            <p class="economia-valor">R$ {{ resultado.economia.valor.toFixed(2) }}</p>
            <p class="economia-percentual">{{ resultado.economia.percentual.toFixed(1) }}% de economia</p>
          </div>
        </div>
      </div>

      <!-- Tabela de Comparação -->
      <div class="comparacao-card">
        <h2>📊 Comparação Detalhada</h2>
        
        <div class="table-container">
          <table class="cotacoes-table">
            <thead>
              <tr>
                <th>Transportadora</th>
                <th>Serviço</th>
                <th>Valor</th>
                <th>Prazo</th>
                <th>Fonte</th>
                <th>Observações</th>
                <th>Ação</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(cotacao, index) in resultado.cotacoes" 
                :key="index"
                :class="{ 'melhor-linha': index === 0 }"
              >
                <td>
                  <strong>{{ cotacao.transportadora }}</strong>
                  <span v-if="index === 0" class="badge-melhor">Melhor</span>
                </td>
                <td>{{ cotacao.servico }}</td>
                <td class="valor-cell">
                  <strong>R$ {{ cotacao.valor.toFixed(2) }}</strong>
                </td>
                <td>{{ cotacao.prazo_dias }} dias</td>
                <td>
                  <span class="badge-fonte" :class="cotacao.fonte">
                    {{ fonteLabel(cotacao.fonte) }}
                  </span>
                </td>
                <td class="obs-cell">{{ cotacao.observacoes || '-' }}</td>
                <td>
                  <button @click="selecionarCotacao(cotacao)" class="btn-selecionar">
                    Selecionar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Gráfico de Comparação -->
      <div class="grafico-card">
        <h2>📈 Comparação Visual</h2>
        <div class="grafico-container">
          <div 
            v-for="(cotacao, index) in resultado.cotacoes.slice(0, 5)" 
            :key="index"
            class="barra-item"
          >
            <div class="barra-label">{{ cotacao.transportadora }}</div>
            <div class="barra-wrapper">
              <div 
                class="barra" 
                :style="{ width: calcularLarguraBarra(cotacao.valor) + '%' }"
                :class="{ 'barra-melhor': index === 0 }"
              >
                <span class="barra-valor">R$ {{ cotacao.valor.toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Estado Vazio -->
    <div v-else-if="!loading" class="empty-state">
      <div class="empty-icon">📦</div>
      <h3>Nenhuma cotação realizada ainda</h3>
      <p>Preencha o formulário acima e clique em "Cotar Frete" para comparar preços</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Consultando transportadoras...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const form = ref({
  origem_cep: '',
  destino_cep: '',
  peso_kg: null,
  altura_cm: 20,
  largura_cm: 20,
  comprimento_cm: 20,
  valor_mercadoria: 0,
  incluir_melhor_envio: true,
  incluir_frenet: true,
  incluir_tabela_propria: true
})

const resultado = ref(null)
const loading = ref(false)

const fonteLabel = (fonte) => {
  const labels = {
    'melhor_envio': 'Melhor Envio',
    'frenet': 'Frenet',
    'tabela_propria': 'Tabela Própria'
  }
  return labels[fonte] || fonte
}

const calcularLarguraBarra = (valor) => {
  if (!resultado.value || !resultado.value.cotacoes.length) return 0
  const maxValor = Math.max(...resultado.value.cotacoes.map(c => c.valor))
  return (valor / maxValor) * 100
}

const cotar = async () => {
  loading.value = true
  resultado.value = null

  try {
    const response = await axios.post('/cotacao-automatica/cotar', form.value)
    
    if (response.data.success) {
      resultado.value = response.data
    } else {
      alert('Erro ao cotar: ' + (response.data.message || 'Erro desconhecido'))
    }
  } catch (error) {
    console.error('Erro ao cotar:', error)
    alert('Erro ao realizar cotação. Verifique os dados e tente novamente.')
  } finally {
    loading.value = false
  }
}

const limparForm = () => {
  form.value = {
    origem_cep: '',
    destino_cep: '',
    peso_kg: null,
    altura_cm: 20,
    largura_cm: 20,
    comprimento_cm: 20,
    valor_mercadoria: 0,
    incluir_melhor_envio: true,
    incluir_frenet: true,
    incluir_tabela_propria: true
  }
  resultado.value = null
}

const selecionarCotacao = (cotacao) => {
  if (confirm(`Deseja selecionar ${cotacao.transportadora} - ${cotacao.servico} por R$ ${cotacao.valor.toFixed(2)}?`)) {
    alert('Cotação selecionada! Integração com pedidos será implementada.')
  }
}
</script>

<style scoped>
.cotacao-automatica {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #666;
  font-size: 1.1rem;
}

.cotacao-form-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.cotacao-form-card h2 {
  margin-bottom: 1.5rem;
  color: #1a1a1a;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-control {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
}

.resultados-section {
  display: grid;
  gap: 2rem;
}

.resumo-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.resumo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.total-cotacoes {
  background: #dbeafe;
  color: #1e40af;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 500;
}

.melhor-opcao {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 2px solid #f59e0b;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.melhor-badge {
  background: #f59e0b;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  display: inline-block;
  font-weight: bold;
  margin-bottom: 1rem;
}

.melhor-content h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #92400e;
}

.melhor-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat .label {
  font-size: 0.9rem;
  color: #78350f;
  margin-bottom: 0.25rem;
}

.stat .value {
  font-size: 1.25rem;
  font-weight: bold;
  color: #92400e;
}

.economia-card {
  background: #d1fae5;
  border: 2px solid #10b981;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.economia-icon {
  font-size: 3rem;
}

.economia-content h4 {
  margin-bottom: 0.5rem;
  color: #065f46;
}

.economia-valor {
  font-size: 2rem;
  font-weight: bold;
  color: #10b981;
  margin-bottom: 0.25rem;
}

.economia-percentual {
  color: #059669;
  font-weight: 500;
}

.comparacao-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.comparacao-card h2 {
  margin-bottom: 1.5rem;
}

.table-container {
  overflow-x: auto;
}

.cotacoes-table {
  width: 100%;
  border-collapse: collapse;
}

.cotacoes-table th {
  background: #f3f4f6;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}

.cotacoes-table td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.melhor-linha {
  background: #fef3c7;
}

.badge-melhor {
  background: #f59e0b;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  margin-left: 0.5rem;
}

.valor-cell {
  font-size: 1.1rem;
  color: #10b981;
}

.badge-fonte {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge-fonte.melhor_envio {
  background: #dbeafe;
  color: #1e40af;
}

.badge-fonte.frenet {
  background: #fce7f3;
  color: #9f1239;
}

.badge-fonte.tabela_propria {
  background: #d1fae5;
  color: #065f46;
}

.obs-cell {
  color: #6b7280;
  font-size: 0.9rem;
}

.btn-selecionar {
  background: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-selecionar:hover {
  background: #059669;
}

.grafico-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.grafico-card h2 {
  margin-bottom: 1.5rem;
}

.grafico-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.barra-item {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 1rem;
  align-items: center;
}

.barra-label {
  font-weight: 500;
  color: #374151;
}

.barra-wrapper {
  background: #f3f4f6;
  border-radius: 8px;
  height: 40px;
  position: relative;
  overflow: hidden;
}

.barra {
  background: #3b82f6;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 1rem;
  transition: width 0.5s ease;
}

.barra-melhor {
  background: #f59e0b;
}

.barra-valor {
  color: white;
  font-weight: bold;
  font-size: 0.9rem;
}

.empty-state {
  background: white;
  border-radius: 12px;
  padding: 4rem 2rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #374151;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #9ca3af;
}

.loading-state {
  background: white;
  border-radius: 12px;
  padding: 4rem 2rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.spinner {
  border: 4px solid #f3f4f6;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
