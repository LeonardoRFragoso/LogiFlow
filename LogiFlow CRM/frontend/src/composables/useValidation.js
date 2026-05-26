/**
 * Composable para validações e máscaras de campos
 */

export function useValidation() {
  
  // ========================================
  // Máscaras
  // ========================================
  
  /**
   * Aplica máscara de CPF: 000.000.000-00
   */
  const maskCPF = (value) => {
    if (!value) return ''
    return value
      .replace(/\D/g, '')
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d{1,2})/, '$1-$2')
      .replace(/(-\d{2})\d+?$/, '$1')
  }

  /**
   * Aplica máscara de CNPJ: 00.000.000/0000-00
   */
  const maskCNPJ = (value) => {
    if (!value) return ''
    return value
      .replace(/\D/g, '')
      .replace(/(\d{2})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d)/, '$1/$2')
      .replace(/(\d{4})(\d{1,2})/, '$1-$2')
      .replace(/(-\d{2})\d+?$/, '$1')
  }

  /**
   * Aplica máscara de CEP: 00000-000
   */
  const maskCEP = (value) => {
    if (!value) return ''
    return value
      .replace(/\D/g, '')
      .replace(/(\d{5})(\d)/, '$1-$2')
      .replace(/(-\d{3})\d+?$/, '$1')
  }

  /**
   * Aplica máscara de telefone: (00) 0000-0000 ou (00) 00000-0000
   */
  const maskPhone = (value) => {
    if (!value) return ''
    const cleaned = value.replace(/\D/g, '')
    if (cleaned.length <= 10) {
      return cleaned
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4})(\d)/, '$1-$2')
        .replace(/(-\d{4})\d+?$/, '$1')
    } else {
      return cleaned
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{5})(\d)/, '$1-$2')
        .replace(/(-\d{4})\d+?$/, '$1')
    }
  }

  /**
   * Aplica máscara de placa: ABC-1234 ou ABC1D23 (Mercosul)
   */
  const maskPlaca = (value) => {
    if (!value) return ''
    const cleaned = value.toUpperCase().replace(/[^A-Z0-9]/g, '')
    if (cleaned.length <= 7) {
      // Formato antigo ou Mercosul
      return cleaned.replace(/([A-Z]{3})([0-9A-Z]{1,4})/, '$1-$2')
    }
    return cleaned.substring(0, 7)
  }

  /**
   * Aplica máscara de moeda: R$ 1.234,56
   */
  const maskMoney = (value) => {
    if (!value && value !== 0) return ''
    const number = typeof value === 'string' 
      ? parseFloat(value.replace(/\D/g, '')) / 100 
      : value
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(number)
  }

  // ========================================
  // Validações
  // ========================================

  /**
   * Valida CPF
   */
  const validateCPF = (cpf) => {
    if (!cpf) return false
    cpf = cpf.replace(/\D/g, '')
    
    if (cpf.length !== 11) return false
    if (/^(\d)\1+$/.test(cpf)) return false
    
    let sum = 0
    for (let i = 0; i < 9; i++) {
      sum += parseInt(cpf.charAt(i)) * (10 - i)
    }
    let digit = 11 - (sum % 11)
    if (digit > 9) digit = 0
    if (parseInt(cpf.charAt(9)) !== digit) return false
    
    sum = 0
    for (let i = 0; i < 10; i++) {
      sum += parseInt(cpf.charAt(i)) * (11 - i)
    }
    digit = 11 - (sum % 11)
    if (digit > 9) digit = 0
    if (parseInt(cpf.charAt(10)) !== digit) return false
    
    return true
  }

  /**
   * Valida CNPJ
   */
  const validateCNPJ = (cnpj) => {
    if (!cnpj) return false
    cnpj = cnpj.replace(/\D/g, '')
    
    if (cnpj.length !== 14) return false
    if (/^(\d)\1+$/.test(cnpj)) return false
    
    let size = cnpj.length - 2
    let numbers = cnpj.substring(0, size)
    let digits = cnpj.substring(size)
    let sum = 0
    let pos = size - 7
    
    for (let i = size; i >= 1; i--) {
      sum += numbers.charAt(size - i) * pos--
      if (pos < 2) pos = 9
    }
    
    let result = sum % 11 < 2 ? 0 : 11 - sum % 11
    if (result !== parseInt(digits.charAt(0))) return false
    
    size = size + 1
    numbers = cnpj.substring(0, size)
    sum = 0
    pos = size - 7
    
    for (let i = size; i >= 1; i--) {
      sum += numbers.charAt(size - i) * pos--
      if (pos < 2) pos = 9
    }
    
    result = sum % 11 < 2 ? 0 : 11 - sum % 11
    if (result !== parseInt(digits.charAt(1))) return false
    
    return true
  }

  /**
   * Valida email
   */
  const validateEmail = (email) => {
    if (!email) return false
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return regex.test(email)
  }

  /**
   * Valida CEP
   */
  const validateCEP = (cep) => {
    if (!cep) return false
    const cleaned = cep.replace(/\D/g, '')
    return cleaned.length === 8
  }

  /**
   * Valida placa de veículo (antiga e Mercosul)
   */
  const validatePlaca = (placa) => {
    if (!placa) return false
    const cleaned = placa.toUpperCase().replace(/[^A-Z0-9]/g, '')
    // Placa antiga: ABC1234 ou Mercosul: ABC1D23
    return /^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$/.test(cleaned)
  }

  // ========================================
  // Utilitários
  // ========================================

  /**
   * Remove máscara e retorna apenas números
   */
  const unmask = (value) => {
    if (!value) return ''
    return value.replace(/\D/g, '')
  }

  /**
   * Formata data para exibição: DD/MM/YYYY
   */
  const formatDate = (date) => {
    if (!date) return ''
    const d = new Date(date)
    return d.toLocaleDateString('pt-BR')
  }

  /**
   * Formata data e hora: DD/MM/YYYY HH:mm
   */
  const formatDateTime = (date) => {
    if (!date) return ''
    const d = new Date(date)
    return d.toLocaleString('pt-BR')
  }

  /**
   * Formata valor monetário
   */
  const formatCurrency = (value) => {
    if (!value && value !== 0) return 'R$ 0,00'
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  /**
   * Busca endereço por CEP via ViaCEP
   */
  const fetchAddressByCEP = async (cep) => {
    const cleaned = cep.replace(/\D/g, '')
    if (cleaned.length !== 8) return null
    
    try {
      const response = await fetch(`https://viacep.com.br/ws/${cleaned}/json/`)
      const data = await response.json()
      
      if (data.erro) return null
      
      return {
        logradouro: data.logradouro,
        bairro: data.bairro,
        cidade: data.localidade,
        uf: data.uf
      }
    } catch (error) {
      console.error('Erro ao buscar CEP:', error)
      return null
    }
  }

  return {
    // Máscaras
    maskCPF,
    maskCNPJ,
    maskCEP,
    maskPhone,
    maskPlaca,
    maskMoney,
    
    // Validações
    validateCPF,
    validateCNPJ,
    validateEmail,
    validateCEP,
    validatePlaca,
    
    // Utilitários
    unmask,
    formatDate,
    formatDateTime,
    formatCurrency,
    fetchAddressByCEP
  }
}
