import { reactive } from 'vue'
import type { Projeto, Tarefa } from './tipos'

// Estado único de busca (e, depois, dos filtros): a lista, o quadro, os projetos
// e a busca geral leem e escrevem aqui. Como vive fora dos componentes, não se
// perde ao trocar de tela.
export const filtros = reactive({
  busca: '',
})

// Ignora maiúsculas e acentos: "diagrama" acha "Diagrama", "repositorio" acha "repositório".
function normalizar(texto: string): string {
  return texto.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
}

function termoBusca(): string {
  return normalizar(filtros.busca.trim())
}

export const temBusca = () => termoBusca() !== ''

export function filtrarTarefas(tarefas: Tarefa[]): Tarefa[] {
  const termo = termoBusca()
  if (!termo) return tarefas
  return tarefas.filter((tarefa) => normalizar(tarefa.titulo).includes(termo))
}

// O "título" de um projeto é o nome dele.
export function filtrarProjetos(projetos: Projeto[]): Projeto[] {
  const termo = termoBusca()
  if (!termo) return projetos
  return projetos.filter((projeto) => normalizar(projeto.nome).includes(termo))
}
