import type { Tarefa } from './tipos'

// Troca a tarefa pelo objeto devolvido pela API.
export function substituirTarefa(tarefas: Tarefa[], nova: Tarefa) {
  const indice = tarefas.findIndex((tarefa) => tarefa.id === nova.id)
  if (indice !== -1) tarefas[indice] = nova
}

// Remove a tarefa da lista.
export function removerTarefa(tarefas: Tarefa[], id: string) {
  const indice = tarefas.findIndex((tarefa) => tarefa.id === id)
  if (indice !== -1) tarefas.splice(indice, 1)
}
