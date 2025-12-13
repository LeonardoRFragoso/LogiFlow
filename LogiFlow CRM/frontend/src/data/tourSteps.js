export const webTourSteps = [
  {
    title: 'Bem-vindo ao LogiFlow CRM! 🚚',
    description: 'Vamos fazer um tour rápido pelas principais funcionalidades do sistema. Este tour levará apenas 2 minutos.',
    route: '/',
    element: null
  },
  {
    title: 'Dashboard Principal',
    description: 'Aqui você tem uma visão geral de todas as operações: pedidos em andamento, entregas do dia, e indicadores de performance.',
    route: '/',
    element: '.dashboard-container'
  },
  {
    title: 'Menu de Navegação',
    description: 'Use este menu lateral para acessar todas as funcionalidades do sistema: Pedidos, Cotações, Motoristas, Veículos e muito mais.',
    route: '/',
    element: '.sidebar'
  },
  {
    title: 'Gestão de Pedidos',
    description: 'Aqui você gerencia todos os pedidos de frete. Crie novos pedidos, acompanhe o status e atribua motoristas.',
    route: '/pedidos',
    element: '.page-header'
  },
  {
    title: 'Filtros Inteligentes',
    description: 'Use os filtros para visualizar pedidos por status, SLA ou outros critérios. Facilita muito a gestão diária!',
    route: '/pedidos',
    element: '.filters-bar'
  },
  {
    title: 'Criar Novo Pedido',
    description: 'Clique aqui para criar um novo pedido de frete. O formulário é simples e intuitivo.',
    route: '/pedidos',
    element: '.btn-add'
  },
  {
    title: 'Gestão de Ocorrências',
    description: 'Registre e acompanhe problemas nas entregas: atrasos, avarias, extravios. Tudo centralizado para melhor controle.',
    route: '/ocorrencias',
    element: '.page-header'
  },
  {
    title: 'Priorização de Ocorrências',
    description: 'As ocorrências são organizadas por prioridade. Resolva primeiro as mais críticas!',
    route: '/ocorrencias',
    element: '.priority-filters'
  },
  {
    title: 'Motoristas',
    description: 'Gerencie sua equipe de motoristas: cadastro, documentação, disponibilidade e histórico de entregas.',
    route: '/motoristas',
    element: '.page-header'
  },
  {
    title: 'Frota de Veículos',
    description: 'Controle completo da frota: manutenções, disponibilidade, capacidade e custos operacionais.',
    route: '/veiculos',
    element: '.page-header'
  },
  {
    title: 'Cotações',
    description: 'Crie e gerencie cotações de frete para seus clientes. Converta cotações aprovadas em pedidos com um clique.',
    route: '/cotacoes',
    element: '.page-header'
  },
  {
    title: 'Configurações',
    description: 'Personalize o sistema, gerencie usuários, configure integrações e ajuste preferências.',
    route: '/sla',
    element: '.page-header'
  },
  {
    title: 'Tour Concluído! 🎉',
    description: 'Você está pronto para usar o LogiFlow CRM! Explore as funcionalidades e aproveite. Se precisar de ajuda, acesse o FAQ no menu.',
    route: '/',
    element: null
  }
]

export const driverAppTourSteps = [
  {
    title: 'Bem-vindo, Motorista! 🚛',
    description: 'Este é seu aplicativo de entregas. Vamos conhecer as principais funcionalidades.',
    route: '/',
    element: null
  },
  {
    title: 'Suas Entregas',
    description: 'Aqui estão todas as suas entregas do dia. Toque em uma entrega para ver os detalhes.',
    route: '/',
    element: '.entregas-list'
  },
  {
    title: 'Status da Entrega',
    description: 'Acompanhe o progresso de cada entrega. Atualize o status conforme avança na rota.',
    route: '/',
    element: '.status-badge'
  },
  {
    title: 'Iniciar Navegação',
    description: 'Toque aqui para abrir o GPS e navegar até o endereço de entrega.',
    route: '/',
    element: '.btn-navigate'
  },
  {
    title: 'Confirmar Entrega',
    description: 'Ao chegar no destino, confirme a entrega, colete assinatura e tire foto do comprovante.',
    route: '/',
    element: '.btn-confirm'
  },
  {
    title: 'Registrar Ocorrência',
    description: 'Se houver algum problema (atraso, recusa, avaria), registre aqui imediatamente.',
    route: '/',
    element: '.btn-ocorrencia'
  },
  {
    title: 'Seu Perfil',
    description: 'Acesse seu perfil para ver estatísticas, histórico de entregas e avaliações.',
    route: '/perfil',
    element: '.profile-card'
  },
  {
    title: 'Pronto para Trabalhar! 💪',
    description: 'Agora você sabe usar o app! Boas entregas e dirija com segurança.',
    route: '/',
    element: null
  }
]
