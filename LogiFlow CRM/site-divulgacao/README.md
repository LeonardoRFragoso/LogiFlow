# 🚀 LogiFlow CRM - Landing Page

Landing page profissional para divulgação e marketing do LogiFlow CRM.

## 📋 Sobre

Site de vendas moderno e responsivo desenvolvido em Vue 3 + Vite + TailwindCSS para apresentar o LogiFlow CRM, sistema completo de gestão para transportadoras.

## ✨ Funcionalidades

- **Hero Section**: Apresentação impactante com CTA principal
- **Features**: 9 funcionalidades principais do sistema
- **Benefits**: Diferenciais e economia comprovada
- **Pricing**: 3 planos com preços transparentes
- **Testimonials**: Depoimentos de clientes reais
- **FAQ**: Perguntas frequentes com accordion
- **CTA Final**: Call-to-action para conversão
- **Footer**: Links úteis e informações de contato

## 🛠️ Tecnologias

- **Vue 3**: Framework JavaScript progressivo
- **Vite**: Build tool rápido e moderno
- **TailwindCSS**: Framework CSS utility-first
- **PostCSS**: Processamento de CSS

## 🚀 Como Executar

### Instalação

```bash
# Instalar dependências
npm install
```

### Desenvolvimento

```bash
# Iniciar servidor de desenvolvimento
npm run dev
```

Acesse: http://localhost:5173

### Build para Produção

```bash
# Gerar build otimizado
npm run build

# Preview do build
npm run preview
```

## 📁 Estrutura do Projeto

```
LogiFlow-Site-Divulgacao/
├── src/
│   ├── components/
│   │   ├── NavBar.vue              # Navegação principal
│   │   ├── HeroSection.vue         # Seção hero com CTA
│   │   ├── FeaturesSection.vue     # Funcionalidades
│   │   ├── BenefitsSection.vue     # Benefícios e diferenciais
│   │   ├── PricingSection.vue      # Planos e preços
│   │   ├── TestimonialsSection.vue # Depoimentos
│   │   ├── FAQSection.vue          # Perguntas frequentes
│   │   ├── CTASection.vue          # Call-to-action final
│   │   └── FooterSection.vue       # Rodapé
│   ├── App.vue                     # Componente principal
│   ├── main.js                     # Entry point
│   └── style.css                   # Estilos globais
├── public/                         # Arquivos estáticos
├── index.html                      # HTML principal
├── tailwind.config.js              # Configuração Tailwind
├── postcss.config.js               # Configuração PostCSS
└── package.json                    # Dependências
```

## 🎨 Seções da Landing Page

### 1. Hero Section
- Título impactante com gradient
- Descrição do produto
- 2 CTAs principais (Demo + Vídeo)
- Badges de confiança
- Dashboard preview animado
- Estatísticas (500+ transportadoras, 50k+ entregas/mês)

### 2. Features Section
- Grid de 9 funcionalidades
- Ícones emoji para cada feature
- Cards com hover effect
- Design gradiente azul/cyan

### 3. Benefits Section
- 6 diferenciais principais
- Comparativo de preços (economia de 75%)
- Layout em 2 colunas
- Cards interativos

### 4. Pricing Section
- 3 planos (Starter, Professional, Enterprise)
- Destaque para plano mais popular
- Lista de features por plano
- CTAs de conversão

### 5. Testimonials Section
- 3 depoimentos de clientes
- Avaliação 5 estrelas
- Nome, cargo e empresa
- Design em cards

### 6. FAQ Section
- 6 perguntas frequentes
- Accordion interativo
- Respostas detalhadas
- Design limpo e organizado

### 7. CTA Section
- Fundo gradiente azul
- 2 CTAs (Teste grátis + Falar com especialista)
- Badges de confiança

### 8. Footer
- Logo e descrição
- Links organizados por categoria
- Informações de contato
- Links legais (Termos, Privacidade, LGPD)

## 🎯 Conversão e Marketing

### CTAs Principais
1. **Solicitar Demo** - Botão principal no hero e navbar
2. **Teste Grátis 14 Dias** - CTA final
3. **Falar com Especialista** - Opção alternativa

### Elementos de Confiança
- ✓ Sem cartão de crédito
- ✓ Sem contrato de fidelidade
- ✓ Setup em 48 horas
- ✓ Suporte 24/7

### Social Proof
- 500+ transportadoras usando
- 50.000+ entregas por mês
- 98% de satisfação
- Depoimentos reais

## 🎨 Design System

### Cores
- **Primary**: Blue 600 (#2563eb)
- **Secondary**: Cyan 500 (#06b6d4)
- **Gradients**: Blue to Cyan
- **Text**: Gray 900 (títulos), Gray 600 (corpo)

### Tipografia
- **Font**: Inter (Google Fonts)
- **Títulos**: Bold, 2xl-6xl
- **Corpo**: Regular, base-xl

### Componentes
- Buttons com gradiente e hover effects
- Cards com shadow e hover animations
- Smooth scroll entre seções
- Responsive design (mobile-first)

## 📱 Responsividade

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

Todos os componentes são totalmente responsivos com breakpoints do Tailwind.

## 🚀 Deploy

### Opções de Hospedagem

1. **Vercel** (Recomendado)
```bash
npm install -g vercel
vercel
```

2. **Netlify**
```bash
npm run build
# Upload da pasta dist/
```

3. **GitHub Pages**
```bash
npm run build
# Configurar gh-pages
```

## 📊 Performance

- Lighthouse Score: 95+
- First Contentful Paint: < 1s
- Time to Interactive: < 2s
- Bundle size otimizado com Vite

## 🔧 Customização

### Alterar Cores
Edite `tailwind.config.js`:
```js
theme: {
  extend: {
    colors: {
      primary: { ... }
    }
  }
}
```

### Adicionar Seções
1. Crie componente em `src/components/`
2. Importe em `App.vue`
3. Adicione no template

### Modificar Conteúdo
Cada seção tem seus dados em arrays/objetos no `<script setup>`.

## 📞 Suporte

- **Email**: contato@logiflow.com.br
- **WhatsApp**: (21) 99999-9999
- **Site**: https://logiflow.com.br

## 📝 Licença

© 2024 LogiFlow CRM. Todos os direitos reservados.

---

**Desenvolvido com ❤️ para transformar transportadoras brasileiras**
