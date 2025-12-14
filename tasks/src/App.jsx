import { useState, useEffect } from 'react'
import initialData from './data/tasks.json'

function App() {
  const [data, setData] = useState(() => {
    const saved = localStorage.getItem('logiflow-tasks')
    return saved ? JSON.parse(saved) : initialData
  })
  const [filter, setFilter] = useState('all')
  const [expandedCategories, setExpandedCategories] = useState(
    initialData.categories.map(c => c.id)
  )

  useEffect(() => {
    localStorage.setItem('logiflow-tasks', JSON.stringify(data))
  }, [data])

  const toggleTask = (categoryId, taskId) => {
    setData(prev => ({
      ...prev,
      categories: prev.categories.map(cat => {
        if (cat.id !== categoryId) return cat
        return {
          ...cat,
          tasks: cat.tasks.map(task => {
            if (task.id !== taskId) return task
            const statusOrder = ['pending', 'in_progress', 'done']
            const currentIndex = statusOrder.indexOf(task.status)
            const nextStatus = statusOrder[(currentIndex + 1) % 3]
            return { ...task, status: nextStatus }
          })
        }
      }),
      lastUpdate: new Date().toISOString().split('T')[0]
    }))
  }

  const toggleCategory = (categoryId) => {
    setExpandedCategories(prev =>
      prev.includes(categoryId)
        ? prev.filter(id => id !== categoryId)
        : [...prev, categoryId]
    )
  }

  const getStats = () => {
    const all = data.categories.flatMap(c => c.tasks)
    const done = all.filter(t => t.status === 'done').length
    const inProgress = all.filter(t => t.status === 'in_progress').length
    const pending = all.filter(t => t.status === 'pending').length
    return { total: all.length, done, inProgress, pending, percent: Math.round((done / all.length) * 100) }
  }

  const getCategoryStats = (category) => {
    const done = category.tasks.filter(t => t.status === 'done').length
    const total = category.tasks.length
    return { done, total, percent: Math.round((done / total) * 100) }
  }

  const stats = getStats()

  const filteredCategories = data.categories.map(cat => ({
    ...cat,
    tasks: cat.tasks.filter(task => {
      if (filter === 'all') return true
      return task.status === filter
    })
  })).filter(cat => cat.tasks.length > 0)

  const resetData = () => {
    if (confirm('Resetar todas as tarefas para o estado inicial?')) {
      setData(initialData)
    }
  }

  const statusColors = {
    done: 'bg-green-500',
    in_progress: 'bg-yellow-500',
    pending: 'bg-gray-400'
  }

  const statusLabels = {
    done: 'Concluído',
    in_progress: 'Em Progresso',
    pending: 'Pendente'
  }

  const priorityColors = {
    high: 'border-l-red-500',
    medium: 'border-l-yellow-500',
    low: 'border-l-blue-500'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                🚛 {data.projectName}
                <span className="text-sm font-normal text-slate-400 bg-slate-700 px-2 py-0.5 rounded">
                  {data.version}
                </span>
              </h1>
              <p className="text-slate-400 text-sm mt-1">
                Task Tracker • Última atualização: {data.lastUpdate}
              </p>
            </div>
            <button
              onClick={resetData}
              className="text-slate-400 hover:text-white text-sm px-3 py-1.5 rounded border border-slate-600 hover:border-slate-500 transition"
            >
              🔄 Resetar
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6">
        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
            <div className="text-3xl font-bold text-white">{stats.percent}%</div>
            <div className="text-slate-400 text-sm">Progresso Total</div>
            <div className="mt-2 h-2 bg-slate-700 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-green-500 to-emerald-400 transition-all duration-500"
                style={{ width: `${stats.percent}%` }}
              />
            </div>
          </div>
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
            <div className="text-3xl font-bold text-green-400">{stats.done}</div>
            <div className="text-slate-400 text-sm">Concluídas</div>
          </div>
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
            <div className="text-3xl font-bold text-yellow-400">{stats.inProgress}</div>
            <div className="text-slate-400 text-sm">Em Progresso</div>
          </div>
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
            <div className="text-3xl font-bold text-slate-400">{stats.pending}</div>
            <div className="text-slate-400 text-sm">Pendentes</div>
          </div>
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
            <div className="text-3xl font-bold text-white">{stats.total}</div>
            <div className="text-slate-400 text-sm">Total de Tarefas</div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex gap-2 mb-6 flex-wrap">
          {['all', 'pending', 'in_progress', 'done'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                filter === f
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {f === 'all' ? '📋 Todas' : 
               f === 'pending' ? '⏳ Pendentes' :
               f === 'in_progress' ? '🔄 Em Progresso' : '✅ Concluídas'}
            </button>
          ))}
        </div>

        {/* Categories */}
        <div className="space-y-4">
          {filteredCategories.map(category => {
            const catStats = getCategoryStats(data.categories.find(c => c.id === category.id))
            const isExpanded = expandedCategories.includes(category.id)
            
            return (
              <div key={category.id} className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
                <button
                  onClick={() => toggleCategory(category.id)}
                  className="w-full px-4 py-3 flex items-center justify-between hover:bg-slate-700/50 transition"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{category.icon}</span>
                    <span className="font-semibold text-white">{category.name}</span>
                    <span className="text-sm text-slate-400">
                      ({catStats.done}/{catStats.total})
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-24 h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-green-500 transition-all duration-300"
                        style={{ width: `${catStats.percent}%` }}
                      />
                    </div>
                    <span className="text-slate-400 text-sm w-10">{catStats.percent}%</span>
                    <span className={`text-slate-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
                      ▼
                    </span>
                  </div>
                </button>
                
                {isExpanded && (
                  <div className="border-t border-slate-700">
                    {category.tasks.map(task => (
                      <div
                        key={task.id}
                        onClick={() => toggleTask(category.id, task.id)}
                        className={`px-4 py-3 flex items-center justify-between hover:bg-slate-700/30 cursor-pointer transition border-l-4 ${priorityColors[task.priority]}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-3 h-3 rounded-full ${statusColors[task.status]}`} />
                          <span className={`${task.status === 'done' ? 'text-slate-500 line-through' : 'text-slate-200'}`}>
                            {task.name}
                          </span>
                        </div>
                        <span className={`text-xs px-2 py-1 rounded ${
                          task.status === 'done' ? 'bg-green-500/20 text-green-400' :
                          task.status === 'in_progress' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-slate-600/50 text-slate-400'
                        }`}>
                          {statusLabels[task.status]}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* Legend */}
        <div className="mt-8 p-4 bg-slate-800/30 rounded-xl border border-slate-700">
          <h3 className="text-white font-medium mb-3">💡 Como usar</h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm text-slate-400">
            <div>
              <p className="mb-2"><strong>Clique em uma tarefa</strong> para alternar seu status:</p>
              <p>Pendente → Em Progresso → Concluído → Pendente</p>
            </div>
            <div>
              <p className="mb-2"><strong>Prioridade</strong> (borda esquerda):</p>
              <p>
                <span className="inline-block w-3 h-3 bg-red-500 rounded mr-1"></span> Alta
                <span className="inline-block w-3 h-3 bg-yellow-500 rounded mx-1 ml-3"></span> Média
                <span className="inline-block w-3 h-3 bg-blue-500 rounded mx-1 ml-3"></span> Baixa
              </p>
            </div>
          </div>
          <p className="text-xs text-slate-500 mt-4">
            Os dados são salvos automaticamente no localStorage do navegador.
          </p>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 mt-8 py-4">
        <div className="max-w-6xl mx-auto px-4 text-center text-slate-500 text-sm">
          LogiFlow CRM Task Tracker © 2024
        </div>
      </footer>
    </div>
  )
}

export default App
