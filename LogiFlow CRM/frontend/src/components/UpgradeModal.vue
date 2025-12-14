<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <button @click="$emit('close')" class="close-btn">✕</button>
      
      <div class="modal-header">
        <h2 class="text-3xl font-bold text-gray-900">🚀 Faça Upgrade do Seu Plano</h2>
        <p class="text-gray-600 mt-2">Escolha o plano ideal para o crescimento da sua operação</p>
      </div>

      <div class="plans-grid">
        <!-- Plano Professional -->
        <div class="plan-card recommended">
          <div class="recommended-badge">⭐ Recomendado</div>
          <h3 class="plan-name">Professional</h3>
          <div class="plan-price">
            <span class="price">R$ 599</span>
            <span class="period">/mês</span>
          </div>
          
          <ul class="features-list">
            <li>✅ Até 15 usuários</li>
            <li>✅ Até 30 veículos</li>
            <li>✅ Pedidos ilimitados</li>
            <li>✅ Emissão de CT-e/MDF-e</li>
            <li>✅ Rastreamento GPS</li>
            <li>✅ WhatsApp integrado</li>
            <li>✅ Suporte prioritário</li>
          </ul>
          
          <button @click="selectPlan('professional')" class="upgrade-btn primary">
            Fazer Upgrade Agora
          </button>
        </div>

        <!-- Plano Enterprise -->
        <div class="plan-card">
          <h3 class="plan-name">Enterprise</h3>
          <div class="plan-price">
            <span class="price">R$ 1.499</span>
            <span class="period">/mês</span>
          </div>
          
          <ul class="features-list">
            <li>✅ Usuários ilimitados</li>
            <li>✅ Veículos ilimitados</li>
            <li>✅ Pedidos ilimitados</li>
            <li>✅ API personalizada</li>
            <li>✅ Integrações customizadas</li>
            <li>✅ Gerente de conta dedicado</li>
            <li>✅ Suporte 24/7 prioritário</li>
            <li>✅ Treinamento presencial</li>
          </ul>
          
          <button @click="selectPlan('enterprise')" class="upgrade-btn secondary">
            Fazer Upgrade Agora
          </button>
        </div>
      </div>

      <div class="modal-footer">
        <p class="text-sm text-gray-600">
          💳 Pagamento seguro via Mercado Pago • 🔒 Dados protegidos • ✅ Cancele quando quiser
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close'])

function selectPlan(plan) {
  // Redirecionar para checkout com plano selecionado
  window.location.href = `/checkout?plan=${plan}&upgrade=true`
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 1.5rem;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: #f3f4f6;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e5e7eb;
  transform: rotate(90deg);
}

.modal-header {
  text-align: center;
  margin-bottom: 2rem;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.plan-card {
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  padding: 2rem;
  position: relative;
  transition: all 0.3s;
}

.plan-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.1);
}

.plan-card.recommended {
  border-color: #3b82f6;
  background: linear-gradient(to bottom, #eff6ff, white);
}

.recommended-badge {
  position: absolute;
  top: -0.75rem;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(to right, #3b82f6, #06b6d4);
  color: white;
  padding: 0.25rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.plan-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: #111827;
  margin-bottom: 1rem;
}

.plan-price {
  margin-bottom: 1.5rem;
}

.price {
  font-size: 2.5rem;
  font-weight: bold;
  background: linear-gradient(to right, #3b82f6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.period {
  font-size: 1.125rem;
  color: #6b7280;
  font-weight: 600;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem 0;
  space-y: 0.75rem;
}

.features-list li {
  padding: 0.5rem 0;
  color: #374151;
  font-size: 0.9375rem;
}

.upgrade-btn {
  width: 100%;
  padding: 1rem;
  border-radius: 0.75rem;
  font-weight: 700;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.upgrade-btn.primary {
  background: linear-gradient(to right, #3b82f6, #06b6d4);
  color: white;
}

.upgrade-btn.primary:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
}

.upgrade-btn.secondary {
  background: #111827;
  color: white;
}

.upgrade-btn.secondary:hover {
  background: #3b82f6;
  transform: scale(1.05);
}

.modal-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}
</style>
