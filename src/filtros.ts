import { reactive } from 'vue'
import type { Tarefa } from './tipos'

// Estado único de busca (e, depois, dos filtros): a lista e o quadro leem e
// escrevem aqui. Como vive fora dos componentes, não se perde ao trocar de visão.
export const filtros = reactive({
  busca: '',
})

export function filtrarTarefas(tarefas: Tarefa[]): Tarefa[] {
  const termo = filtros.busca.trim().toLowerCase()
  if (!termo) return tarefas
  return tarefas.filter((tarefa) =>
    [tarefa.titulo, tarefa.descricao, tarefa.responsavel].some((campo) =>
      campo.toLowerCase().includes(termo),
    ),
  )
}