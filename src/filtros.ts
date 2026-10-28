import { reactive } from 'vue'
import type { Prioridade, Projeto, Status, Tarefa } from './tipos'

// Estado único de busca e filtros: a lista, o quadro, os projetos e a busca
// geral leem e escrevem aqui. Como vive fora dos componentes, não se perde ao
// trocar de tela. Status e prioridade vazios ('') significam "todos".
export const filtros = reactive({
  busca: '',
  status: '' as Status | '',
  prioridade: '' as Prioridade | '',
})

// Ignora maiúsculas e acentos: "diagrama" acha "Diagrama", "repositorio" acha "repositório".
function normalizar(texto: string): string {
  return texto.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase()
}

function termoBusca(): string {
  return normalizar(filtros.busca.trim())
}

export const temBusca = () => termoBusca() !== ''
export const temFiltros = () => filtros.status !== '' || filtros.prioridade !== ''

export function limparFiltros() {
  filtros.status = ''
  filtros.prioridade = ''
}

// Busca, status e prioridade se combinam: a tarefa precisa passar em todos.
export function filtrarTarefas(tarefas: Tarefa[]): Tarefa[] {
  const termo = termoBusca()
  return tarefas.filter(
    (tarefa) =>
      (!termo || normalizar(tarefa.titulo).includes(termo)) &&
      (!filtros.status || tarefa.status === filtros.status) &&
      (!filtros.prioridade || tarefa.prioridade === filtros.prioridade),
  )
}

// O "título" de um projeto é o nome dele. Projetos não têm status nem
// prioridade, então só a busca vale para eles.
export function filtrarProjetos(projetos: Projeto[]): Projeto[] {
  const termo = termoBusca()
  if (!termo) return projetos
  return projetos.filter((projeto) => normalizar(projeto.nome).includes(termo))
}
